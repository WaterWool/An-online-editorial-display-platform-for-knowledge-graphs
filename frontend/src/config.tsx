import { ElButton, ElInput } from "element-plus";
import { createEditorConfig, EditorBlockData } from "./packages/editor.utils";
import { createEditorColorProp, createEditorInputProp, createEditorSelectProp, createEditorSliderProp, createEditorTableProp } from "./packages/editor.props";



export const Config = createEditorConfig()


// Config.registry('text', {
//     label: '文本',
//     preview: () => <div>预览文本</div>,
//     render: ({props}) => <span style={{color: props.color || '#000000', fontSize: props.size}}>
//         {props.text|| 'EasyKG'}
//     </span>,
//     props: {
//         text: createEditorInputProp('显示文本'),
//         color: createEditorColorProp('字体颜色'),
//         size: createEditorSelectProp('字体大小', [
//             {label: '12px', val: '12px'},
//             {label: '14px', val: '14px'},
//             {label: '16px', val: '16px'},
//             {label: '18px', val: '18px'},
//             {label: '20px', val: '20px'},
//             {label: '22px', val: '22px'},
//             {label: '24px', val: '24px'},
//         ])
//     }
// })

Config.registry('node', {
    label: '默认节点',
    preview: () => <ElButton circle style={"width: 80px; height: 80px;"}>普通节点</ElButton>,
    render: ({props}) => <ElButton circle type={props.type} style={"width:"+`${props.size || 80}`+"px;height:"+`${props.size || 80}`+"px;"}>
        {props.text || '节点'}
    </ElButton>,
    props: {
        text: createEditorInputProp('节点名称'),
        type: createEditorSelectProp('节点颜色', [
            {label: '默认',  val: '' },
            {label: '蓝色',  val: 'primary'},
            {label: '绿色',  val: 'success'},
            {label: '黄色',  val: 'warning'},
            {label: '红色',  val: 'danger'},
            {label: '灰色',  val: 'info'},
        ]),
        size: createEditorSliderProp('节点大小'),
        classes: createEditorSelectProp('Schema类别', [
            {label: '无', val:'Null'},
            {label: '创意作品-CreativeWork', val: 'CreativeWork'},
            {label: '事件-Event', val:'Event'},
            {label: '无形事物-Intangible', val:'Intangible'},
            {label: '医学实体-MedicalEntity', val:'MedicalEntity'},
            {label: '组织-Organization', val:'Organization'},
            {label: '人-Person', val:'Person'},
            {label: '地点-Place', val:'Place'},
            {label: '产品-Product', val:'Product'},
        ]),
        data: createEditorTableProp('Data属性',{
            options: [
                {key: '键', value: 'key'},
                {key: '值', value: 'value'},
                {key: '备注(可选)', value: 'commnets'},
            ],
            showKey: 'key',
            showValue: 'value',
        }),
    }
})

Config.registry('impnode',{
    label: '重要节点',
    preview: () => <ElButton circle type="primary" style={"width: 80px; height: 80px;"}> 重要节点 </ElButton>,
    render: ({props}) => <ElButton circle type={props.type || "primary"} style={"width:"+`${props.size || 80}`+"px;height:"+`${props.size || 80}`+"px;"}>
        {props.text || '节点'}
    </ElButton>,
    props: {
        text: createEditorInputProp('节点名称'),
        type: createEditorSelectProp('节点颜色', [
            {label: '默认',  val: '' },
            {label: '蓝色',  val: 'primary'},
            {label: '绿色',  val: 'success'},
            {label: '黄色',  val: 'warning'},
            {label: '红色',  val: 'danger'},
            {label: '灰色',  val: 'info'},
        ]),
        size: createEditorSliderProp('节点大小'),
        classes: createEditorSelectProp('Schema类别', [
            {label: '无', val:'Null'},
            {label: '创意作品-CreativeWork', val: 'CreativeWork'},
            {label: '事件-Event', val:'Event'},
            {label: '无形事物-Event', val:'Intangible'},
            {label: '医学实体-MedicalEntity', val:'MedicalEntity'},
            {label: '组织-Organization', val:'Organization'},
            {label: '人-Person', val:'Person'},
            {label: '地点-Place', val:'Place'},
            {label: '产品-Product', val:'Product'},
        ]),
        data: createEditorTableProp('Data属性',{
            options: [
                {key: '键', value: 'key'},
                {key: '值', value: 'value'},
                {key: '备注(可选)', value: 'commnets'},
            ],
            showKey: 'key',
            showValue: 'value',
        }),
    }
})

Config.registry('dgnode',{
    label: '警告节点',
    preview: () => <ElButton circle type="danger" style={"width: 80px; height: 80px;"}> 警告节点 </ElButton>,
    render: ({props}) => <ElButton circle type={props.type || "danger"} style={"width:"+`${props.size || 80}`+"px;height:"+`${props.size || 80}`+"px;"}>
        {props.text || '节点'}
    </ElButton>,
    props: {
        text: createEditorInputProp('节点名称'),
        type: createEditorSelectProp('节点颜色', [
            {label: '默认',  val: '' },
            {label: '蓝色',  val: 'primary'},
            {label: '绿色',  val: 'success'},
            {label: '黄色',  val: 'warning'},
            {label: '红色',  val: 'danger'},
            {label: '灰色',  val: 'info'},
        ]),
        size: createEditorSliderProp('节点大小'),
        classes: createEditorSelectProp('Schema类别', [
            {label: '无', val:'Null'},
            {label: '创意作品-CreativeWork', val: 'CreativeWork'},
            {label: '事件-Event', val:'Event'},
            {label: '无形事物-Event', val:'Intangible'},
            {label: '医学实体-MedicalEntity', val:'MedicalEntity'},
            {label: '组织-Organization', val:'Organization'},
            {label: '人-Person', val:'Person'},
            {label: '地点-Place', val:'Place'},
            {label: '产品-Product', val:'Product'},
        ]),
        data: createEditorTableProp('Data属性',{
            options: [
                {key: '键', value: 'key'},
                {key: '值', value: 'value'},
                {key: '备注(可选)', value: 'commnets'},
            ],
            showKey: 'key',
            showValue: 'value',
        }),
    }
})

Config.registry('graynode',{
    label: '灰色节点',
    preview: () => <ElButton circle type="info" style={"width: 80px; height: 80px;"}> 灰色节点 </ElButton>,
    render: ({props}) => <ElButton circle type={props.type || "info"} style={"width:"+`${props.size || 80}`+"px;height:"+`${props.size || 80}`+"px;"}>
        {props.text || '节点'}
    </ElButton>,
    props: {
        text: createEditorInputProp('节点名称'),
        type: createEditorSelectProp('节点颜色', [
            {label: '默认',  val: '' },
            {label: '蓝色',  val: 'primary'},
            {label: '绿色',  val: 'success'},
            {label: '黄色',  val: 'warning'},
            {label: '红色',  val: 'danger'},
            {label: '灰色',  val: 'info'},
        ]),
        size: createEditorSliderProp('节点大小'),
        classes: createEditorSelectProp('Schema类别', [
            {label: '无', val:'Null'},
            {label: '创意作品-CreativeWork', val: 'CreativeWork'},
            {label: '事件-Event', val:'Event'},
            {label: '无形事物-Event', val:'Intangible'},
            {label: '医学实体-MedicalEntity', val:'MedicalEntity'},
            {label: '组织-Organization', val:'Organization'},
            {label: '人-Person', val:'Person'},
            {label: '地点-Place', val:'Place'},
            {label: '产品-Product', val:'Product'},
        ]),
        data: createEditorTableProp('Data属性',{
            options: [
                {key: '键', value: 'key'},
                {key: '值', value: 'value'},
                {key: '备注(可选)', value: 'commnets'},
            ],
            showKey: 'key',
            showValue: 'value',
        }),
    }
}) 

/* Config.registry('input', {
    label: '输入框',
    preview: () => <ElInput>预览</ElInput>,
    render: () => <ElInput>渲染</ElInput>
}) */

/* Config.registry('select', {
    label: '下拉框',
    preview: () => <ElSelect/>,
    render: ({props}) => <ElSelect>
        {(props.options || []).map((opt: {key:string, value: string}, index:number) => (
            <ElOption label={opt.key} value={opt.value} key={index}/>
        ))}
    </ElSelect>,
    props: {
        options: createEditorTableProp('下拉选项',{
            options: [
                {value: 'value', key: '属性'},
                {value: 'key', key: '值'},
            ],
            showKey: 'label',
            showValue: 'value'
        }),
        
    },

}) */
