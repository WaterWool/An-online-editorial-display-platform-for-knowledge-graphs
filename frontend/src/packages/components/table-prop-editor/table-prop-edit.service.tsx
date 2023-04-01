import { EditorProps } from "@/packages/editor.props"
import { defer } from "@/packages/utils/defer"
import deepcopy from "deepcopy"
import { ElButton, ElDialog, ElInput, ElTable, ElTableColumn } from "element-plus"
import { defineComponent, getCurrentInstance, onMounted, PropType, reactive, createApp } from "vue"

export interface TablePropEditorServiceOption {
    data: any[],
    config: EditorProps,
    onConfirm: (val: AnimationPlaybackEvent[]) => void,
}

const ServiceComponent = defineComponent({
    props: {
        option: { type: Object as PropType<TablePropEditorServiceOption>, require: true },
    },
    setup(props) {

        const ctx = getCurrentInstance()!

        const state = reactive({
            option: props.option,
            showFlag: false,
            mounted: (() => {
                const dfd = defer()
                onMounted(() => setTimeout(() => dfd.resolve(), 0))
                return dfd.promise
            })(),
            editData: [] as any[],
        })

        const methods = {
            service: (option: TablePropEditorServiceOption) => {
                state.option = option
                state.editData = deepcopy(option.data || [])
                methods.show()
            },
            show: async () => {
                await state.mounted
                state.showFlag = true
            },
            hide: () => {
                state.showFlag = false
            },
            add: () => {
                state.editData.push({})
            },
            reset: () => {
                state.editData = deepcopy(state.option?.data || [])
            },
        }

        const handler = {
            onConfirm: () => {
                state.option?.onConfirm(state.editData)
                methods.hide()
            },
            onCancel: () => {
                methods.hide()
            },
            onDelete: (index: number) => {
                state.editData.splice(index, 1)
            },
        }

        Object.assign(ctx.proxy!, methods)

        return () =>
            // eslint-disable-next-line @typescript-eslint/ban-ts-comment
            // @ts-ignore
            <ElDialog v-model={state.showFlag}>
                {{
                    default: () => (
                        <div>
                            <div >
                                <ElButton {...{onClick:methods.add} as any}>添加</ElButton>
                                <ElButton {...{onClick:methods.reset} as any}>重置</ElButton>
                            </div>
                            <ElTable data={state.editData}>
                                <ElTableColumn {...{ type: 'index' } as any} />
                                {state.option?.config.table!.options.map((item, _index) => (
                                    <ElTableColumn {...{ label: item.key } as any}>
                                        {{
                                            default: ({ row }: { row: any }) => <ElInput v-model={row[item.value]} />
                                        }}
                                    </ElTableColumn>
                                ))}
                                <ElTableColumn {...{ label: '操作'} as any}>
                                {{
                                    default: ({$index}: { $index: number }) => <ElButton
                                        type="danger" {...{onClick: () => handler.onDelete($index)} as any}>
                                        删除
                                    </ElButton>
                                }}
                                </ElTableColumn>
                            </ElTable>
                        </div>
                    ),
                    footer: () => <>
                        <ElButton type="primary" {...{onClick:handler.onConfirm} as any}>确定</ElButton>
                        <ElButton {...{onClick:handler.onCancel} as any}>取消</ElButton>
                    </>
                }}
            </ElDialog>
    }
})

export const $$tablePropEditor = (() => {
    let ins: any;
    return (option: Omit<TablePropEditorServiceOption, 'onConfirm'>) => {
        if (!ins) {
            const el = document.createElement('div')
            document.body.appendChild(el)
            const app = createApp(ServiceComponent, { option })
            ins = app.mount(el)
        }
        const dfd = defer<any[]>()
        ins.service({
            ...option,
            onConfirm: dfd.resolve,
        })
        return dfd.promise
    }
})()

