import { EditorProps } from "@/packages/editor.props"
import { useModel } from "@/packages/useModel"
import { ElButton, ElTag } from "element-plus"
import { defineComponent, PropType } from "vue"
import { $$tablePropEditor } from "./table-prop-edit.service"
import "./table-prop-editor.scss"

export const TablePropEditor = defineComponent({
    props: {
        modelValue: { type: Array as PropType<any[]> },
        propConfig: { type: Object as PropType<EditorProps>, required: true },
    },
    emits: {
        'update:modelValue': (_val?: any[]) => true,
    },
    setup(props, ctx) {

        const model = useModel(() => props.modelValue, val => ctx.emit('update:modelValue', val))

        const onClick = async () => {
            const data = await $$tablePropEditor({
                config: props.propConfig,
                data: props.modelValue || [],
            })
            model.value = data
        }

        return () => (
            <div>
                {(!model.value || model.value.length == 0) && <ElButton {...{ onClick } as any} style={'width:100%'}>
                    添加
                </ElButton>}
                {(model.value || []).map(item => (
                    <ElTag {...{ onClick } as any}>
                        {item[props.propConfig.table!.showKey]}: {item[props.propConfig.table!.showValue]}
                    </ElTag>
                ))}
            </div>
        )

    }

})