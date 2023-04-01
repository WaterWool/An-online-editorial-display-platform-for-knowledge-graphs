import { createApp, defineComponent, getCurrentInstance, PropType, reactive } from "vue"
import { defer } from "./defer"
import { ElInput, ElDialog, ElButton } from "element-plus"

enum DialogServiceEditType {
    textarea = 'textarea',
    input = 'input'
}

interface DialogServiceOption {
    title?: string,
    editType: DialogServiceEditType,
    editReadonly?: boolean,
    editValue?: string | null,
    // editValue是一个动态挂载的响应式变量。
    // element-plus里边的dialog不能接受静态的数据。
    onConfirm: (val?: string | null) => void,
}

const keyGenerator = (() => {
    let count = 0
    return () => `auto_key${count++}`
})();

const ServiceComponnet = defineComponent({

    props: {
        option: { type: Object as PropType<DialogServiceOption>, required: true },
    },

    setup(props) {

        const ctx = getCurrentInstance()!

        const state = reactive({
            option: props.option,
            editValue: null as undefined | null | string,
            showFlag: false,
            key: keyGenerator(),
        })

        const methods = {
            service: (option: DialogServiceOption) => {
                state.option = option
                state.editValue = option.editValue
                state.key = keyGenerator()
                methods.show()  //?
            },
            show: () => {
                state.showFlag = true
            },
            hide: () => state.showFlag = false,
        }

        const handler = {
            onConfirm: () => {
                state.option.onConfirm(state.editValue)
                methods.hide()
            },
            onCancel: () => {
                methods.hide()
            }
        }

        Object.assign(ctx.proxy, methods)

        return () => (
            // eslint-disable-next-line
            // @ts-ignore
            <ElDialog v-model={state.showFlag} title={state.option.title} key={state.key}> {/* 这一块有严重的报错，不过还是没有弄明白是为什么，暂时注释掉吧 */}
                {{
                    default: () => (<div>
                        {state.option.editType === DialogServiceEditType.textarea ? (
                            <ElInput type='textarea' {...{ rows: 10 }} v-model={state.editValue}></ElInput>
                        ) : (
                            <ElInput v-model={state.editValue}></ElInput>
                        )}
                    </div>),
                    footer: () => (<div>
                        <ElButton {...{ onClick: handler.onCancel as any }}>取消</ElButton>
                        <ElButton type="primary" {...{ onClick: handler.onConfirm as any }}>确定</ElButton>
                    </div>)
                }}
            </ElDialog>
        )
    }
})


const DialogService = (() => {
    let ins: any;
    return (option: DialogServiceOption) => {
        if (!ins) {
            const el = document.createElement('div')
            document.body.appendChild(el)
            const app = createApp(ServiceComponnet, { option })
            ins = app.mount(el)
        }
        ins.service(option)
    }
})();

export const $$dialog = Object.assign(DialogService, {
    input: (initValue?: string, title?: string, option?: Omit<DialogServiceOption,'editType' | 'onConfirm'>) => {
        const dfd = defer<string | null | undefined>()
        const opt: DialogServiceOption = {
            ...option,
            editType: DialogServiceEditType.input, 
            onConfirm: dfd.resolve, 
            editValue: initValue,
            title
        }
        DialogService(opt)
        return dfd.promise
    },
    textarea: (initValue?: string, title?: string, option?: Omit<DialogServiceOption,'editType' | 'onConfirm'>) => {
        const dfd = defer<string | null | undefined>()
        const opt: DialogServiceOption =  {
            ...option,
            editType: DialogServiceEditType.textarea, 
            onConfirm: dfd.resolve, 
            editValue: initValue,
            title 
        }
        DialogService(opt)
        return dfd.promise
    },
})