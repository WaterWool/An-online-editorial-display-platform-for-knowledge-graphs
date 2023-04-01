export enum EditorPropsType {
    input = 'input',
    color = 'color',
    select = 'select',
    slider = 'slider',
    table = "table"
}

export type EditorProps = {
    type: EditorPropsType,
    label: string,
} & {
    options?: EditorSelectOptions,
} & {
    table?: EditorTableOption,
}

// 文本input
export function createEditorInputProp(label: string): EditorProps {
    return {
        type: EditorPropsType.input,
        label,
    }
}

// 颜色color
export function createEditorColorProp(label: string): EditorProps {
    return {
        type: EditorPropsType.color,
        label,
    }
}

// 复选框select
export type EditorSelectOptions = {
    label: string,
    val: string,
}[]
export function createEditorSelectProp(label: string, options: EditorSelectOptions): EditorProps {
    return {
        type: EditorPropsType.select,
        label,
        options,
    }
}

// 滑动条Slider
export function createEditorSliderProp(label: string): EditorProps {
    return {
        type: EditorPropsType.slider,
        label,
    }
}

// 表格table
 export type EditorTableOption = {
    options: {
        key: string,
        value: string,
    }[],
    showKey: string,
    showValue: string,
 }

 export function createEditorTableProp(label: string, option: EditorTableOption): EditorProps {
     return {
         type: EditorPropsType.table,
         label,
         table: option,
     }
 }