import deepcopy from "deepcopy";
import { ElColorPicker, ElForm, ElFormItem, ElInput, ElInputNumber, ElSelect, ElOption, ElButton, ElSlider, ElDivider, ElTable } from "element-plus";
import { defineComponent, PropType, reactive, watch } from "vue";
import { TablePropEditor } from "./components/table-prop-editor/table-prop-editor";
import { EditorProps, EditorPropsType } from "./editor.props";
import { EditorBlockData, EditorConfig, EditorModelValue } from "./editor.utils";

export const EditorOperator = defineComponent({
    props: {
        block: { type: Object as PropType<EditorBlockData> },
        config: { type: Object as PropType<EditorConfig>, required: true },
        dataModel: { type: Object as PropType<{ value: EditorModelValue }>, required: true },
        updateBlock: { type: Function as PropType<((newBlock: EditorBlockData, oldBlock: EditorBlockData) => void)>, required: true },
        updateModelValue: {
            type: Function as PropType<((vali: EditorModelValue) => void)>,
            required: true
        }
    },
    setup(props) {

        const state = reactive({
            editData: {} as any,
        })

        const methods = {
            apply: () => {
                if (!props.block) {
                    /*当前编辑容器属性*/
                    props.updateModelValue({
                        ...props.dataModel.value,
                        container: state.editData,
                    })
                } else {
                    /*当前编辑block数据的属性*/
                    props.updateBlock({
                        ...props.block,
                        props: state.editData,
                    }, props.block)
                }
            },
            reset: () => {
                if (!props.block) {
                    state.editData = deepcopy(props.dataModel.value.container)
                } else {
                    state.editData = deepcopy(props.block.props || {})
                }
            },
        }

        watch(() => props.block, () => {
            methods.reset()
        }, { immediate: true })

        const renderEditor = (propName: string, propConfig: EditorProps) => {
            return {
                [EditorPropsType.input]: () => (<ElInput v-model={state.editData[propName]} />),
                [EditorPropsType.color]: () => (<ElColorPicker v-model={state.editData[propName]} />),
                [EditorPropsType.select]: () => (<ElSelect v-model={state.editData[propName]}>
                    {(() => {
                        return propConfig.options!.map(opt => (
                            <ElOption label={opt.label} value={opt.val} />
                        ))
                    })()}
                </ElSelect>),
                [EditorPropsType.slider]: () => (<ElSlider v-model={state.editData[propName]}
                    {...{
                        min: 40,
                        max: 120,
                        step: 10,
                        formatTooltip: ((val) => { return val + 'px' })
                    }} />),
                [EditorPropsType.table]: () => (
                <TablePropEditor 
                    v-model={state.editData[propName]}
                    propConfig={propConfig}
                />)
            }[propConfig.type]()
        }

        return () => {

            let content: JSX.Element | null = null;

            if (!props.block) {
                content = <>
                    <ElFormItem label="画布宽度">
                        <ElInputNumber v-model={state.editData.width} {... { step: 100 } as any} />
                    </ElFormItem>
                    <ElFormItem label="画布高度">
                        <ElInputNumber v-model={state.editData.height} {... { step: 100 } as any} />
                    </ElFormItem>
                </>
            } else {
                const { componentKey } = props.block
                const component = props.config.componentMap[componentKey]
                if (!!component && !!component.props) {                  
                    content = <>
                        {Object.entries(component.props || {}).map(([propName, propConfig]) => {
                            return <ElFormItem label={propConfig.label} key={propName}>
                                {renderEditor(propName, propConfig)}
                            </ElFormItem>
                        })}
                    </>
                }
            }

            return (
                <div class="editor-operator">
                    <ElForm labelPosition="top">
                        {content}
                        <ElFormItem>
                            <el-tooltip effect="light" content="将修改的内容应用到数据中" placement="top">
                                <ElButton {...{ onClick: methods.apply } as any} type="primary">应用</ElButton>
                            </el-tooltip>
                            <el-tooltip effect="light" content="重置到上一次应用时的状态" placement="top">
                                <ElButton {...{ onClick: methods.reset } as any}>重置</ElButton>
                            </el-tooltip>
                        </ElFormItem>
                    </ElForm>
                    
                </div>
                
            )
        }
    }
})