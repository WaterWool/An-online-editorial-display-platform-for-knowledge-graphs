import { EditorProps } from "./editor.props";
import { arrowList, expState } from "./editor";

export interface EditorBlockData {
    componentKey: string,
    top: number,
    left: number,
    adjustPosition: boolean,
    focus: boolean, //是否被选中
    zIndex: number,
    // width: number,
    // height: number,
    hasResize: boolean, //是否被调整过大小
    props: EditorBlockDataProps  //组件的设计属性
}

export interface EditorBlockDataProps {
    size?: number
}

export interface EditorArrowData {
    num_start: number,
	num_end: number,
	text: string
}

export interface EditorModelValue {
    container: {
        width: number,
        height: number
    },
    blocks?: EditorBlockData[]
    arrows?: EditorArrowData[]
}

export interface EditorComponent {
    key: string,
    label: string,
    preview: () => JSX.Element,
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    render: (data: { props: any }) => JSX.Element,
    props?: Record<string, EditorProps>
    data?: Record<string, unknown>
}

export interface EditorMarkLines {
    x: { left: number, showLeft: number }[],
    y: { top: number, showTop: number }[]
}

export interface EditorArrowList {
    num_start: number,
    num_end: number,
	text: string,
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
	arrow: any,
	arrowNum: number,
	arrowId: string,
	arrowTextId: string,
	removed: boolean,  //是否被删除
	focus: boolean
}

export interface EditorArrowMoveList {
    num_start: number,
    num_end: number,
	text: string,
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
	arrow: any,
	arrowNum: number,
	arrowId: string,
	arrowTextId: string,
	removed: boolean,
	focus: boolean,
	index_move: number  //在arrowlist数组中的标号
}

export function createNewBlock(
    {
        component,
        left,
        top,
    }: {
        component: EditorComponent,
        top: number,
        left: number,
    }): EditorBlockData {
    return {
        top,
        left,
        componentKey: component.key,
        adjustPosition: true,
        focus: false,
        zIndex: 3,
        
        hasResize: false,
        props: {},
    }
}
// eslint-disable-next-line @typescript-eslint/no-explicit-any
export function createNewArrow(jsonArrow: EditorArrowData, blocks: EditorBlockData[] | undefined, container: HTMLDivElement): any {
	const editorContent = document.getElementById('editor-content')
	const editorContainer = document.getElementById('editor-container')// eslint-disable-next-line @typescript-eslint/no-explicit-any
	const LeaderLine: any = require("./plugins/leader-line.min.js")  //在不写对应的.d.ts文件的情况下，js文件不能通过es6的export/import导出引入，应该使用es5的module.exports和require导出引入
	const block_start :EditorBlockData = (blocks || [])[jsonArrow.num_start]
	const block_end :EditorBlockData = (blocks || [])[jsonArrow.num_end]
	const r1 = (block_start.props.size || 80) / 2
	const r2 = (block_end.props.size || 80) / 2
	const x1 = block_start.left + r1
	const y1 = block_start.top + r1
	const x2 = block_end.left + r2
	const y2 = block_end.top + r2
	const d = Math.sqrt((x2-x1)*(x2-x1) + (y2-y1)*(y2-y1))
	if (editorContent && editorContainer) {
		const arrow_start_x = (x2-x1)*r1/d + x1 - editorContainer.offsetLeft + editorContent.scrollLeft
		const arrow_start_y = (y2-y1)*r1/d + y1 - editorContainer.offsetTop + editorContent.scrollTop
		const arrow_end_x = x2 - (x2-x1)*r2/d - editorContainer.offsetLeft + editorContent.scrollLeft
		const arrow_end_y = y2 - (y2-y1)*r2/d - editorContainer.offsetTop + editorContent.scrollTop
		const arrow = new LeaderLine(LeaderLine.pointAnchor(container, {x: arrow_start_x, y: arrow_start_y}), LeaderLine.pointAnchor(container, {x: arrow_end_x, y: arrow_end_y}))
        // arrow.middleLabel = LeaderLine.captionLabel('默认',{fontSize: 12})
        arrow.path = 'straight'  //将箭头的路径设置为直线
        // arrow.path = 'magnet'
        arrow.color = '#828282'  //$itc: #314659 字体颜色
        arrow.size = 1
        arrow.endPlugSize = 2
        arrow.showEffectName = 'draw'
        return arrow
    }
}

// eslint-disable-next-line @typescript-eslint/no-explicit-any
export function createNewArrowText(jsonArrow: EditorArrowData, arrowNum: number, blocks: EditorBlockData[] | undefined, container: HTMLDivElement, blockClearFocus: (block?: EditorBlockData) => void, arrowClearAllFocus: () => void): any { //该函数写了修改箭头文字，而createNewArrowTextMouse函数没有写修改箭头文字，因为是用不到的
	const editorContent = document.getElementById('editor-content')
	const editorContainer = document.getElementById('editor-container')
	const LeaderLine: any = require("./plugins/leader-line.min.js")  //在不写对应的.d.ts文件的情况下，js文件不能通过es6的export/import导出引入，应该使用es5的module.exports和require导出引入
	const block_start :EditorBlockData = (blocks || [])[jsonArrow.num_start]
	const block_end :EditorBlockData = (blocks || [])[jsonArrow.num_end]
	const r1 = (block_start.props.size || 80) / 2
	const r2 = (block_end.props.size || 80) / 2
	const x1 = block_start.left + r1
	const y1 = block_start.top + r1
	const x2 = block_end.left + r2
	const y2 = block_end.top + r2
	const d = Math.sqrt((x2-x1)*(x2-x1) + (y2-y1)*(y2-y1))
	if (editorContent && editorContainer) {
		// eslint-disable-next-line @typescript-eslint/no-explicit-any
		const arrow_start_x = (x2-x1)*r1/d + x1
		const arrow_start_y = (y2-y1)*r1/d + y1
		const arrow_end_x = x2 - (x2-x1)*r2/d
		const arrow_end_y = y2 - (y2-y1)*r2/d
		
		const div = document.createElement("div")
		div.id = 'arrowText' + arrowNum
		div.className = 'arrow-text'
		div.style.position = "absolute"
		div.style.zIndex = "2"
		div.innerHTML = jsonArrow.text
		editorContainer.appendChild(div)
		div.style.left = `${(arrow_start_x + arrow_end_x)/2 - div.clientWidth/2}px`
		div.style.top = `${(arrow_start_y + arrow_end_y)/2 - div.clientHeight/2}px`
		
		const changeText = (e: MouseEvent) => {
			if(expState.editing === false)
				return
			
			div.removeEventListener("click", changeText)
			
			if (!e.shiftKey){  // || state.addArrow
				blockClearFocus()
				arrowClearAllFocus()
			}
			arrowList.forEach((arrowInformation: EditorArrowList, index: number) => {
				if (arrowInformation.arrowTextId === 'arrowText' + arrowNum) {
					arrowInformation.focus = true
					arrowInformation.arrow.dash = {animation: true, len: 4 , gap: 4}
				}
			})
			const inputDiv = document.createElement("div")
			inputDiv.id = 'arrowText' + arrowNum
			inputDiv.style.position = "absolute"
			inputDiv.style.zIndex = "9990"
			const cWidth = div.clientWidth + 12
			const cHeight = div.clientHeight + 6
			inputDiv.innerHTML = `<input id=${'arrowTextInput' + arrowNum} type="text" class="label-editor" style="width: ${cWidth}px; height: ${cHeight}px;">`
			editorContainer.appendChild(inputDiv)
			inputDiv.style.left = `${(arrow_start_x + arrow_end_x)/2 - inputDiv.clientWidth/2}px`
			inputDiv.style.top = `${(arrow_start_y + arrow_end_y)/2 - inputDiv.clientHeight/2}px`
			const arrowTextInput = document.getElementById('arrowTextInput' + arrowNum) as HTMLInputElement
			if(arrowTextInput){
				setTimeout(() => {arrowTextInput.focus()}, 10)  //这里需要延时，不然输入框会失去焦点
				arrowTextInput.value = jsonArrow.text
			}
			div.remove()
		}
		div.addEventListener("click", changeText)
		return div
	}
}

export function createNewArrowMouse(num_start: number, clientX: number, clientY: number, blocks: EditorBlockData[] | undefined, container: HTMLDivElement): any {  //js中不存在重载
	const editorContent = document.getElementById('editor-content')
	const editorContainer = document.getElementById('editor-container')
	if(editorContent && editorContainer){
		// eslint-disable-next-line @typescript-eslint/no-explicit-any
		const LeaderLine: any = require("./plugins/leader-line.min.js")  //在不写对应的.d.ts文件的情况下，js文件不能通过es6的export/import导出引入，应该使用es5的module.exports和require导出引入
		const block_start :EditorBlockData = (blocks || [])[num_start]
		const r1 = (block_start.props.size || 80) / 2
		const x1 = block_start.left + r1
		const y1 = block_start.top + r1
		const x2 = clientX - editorContainer.offsetLeft + editorContent.scrollLeft
		const y2 = clientY - editorContainer.offsetTop + editorContent.scrollTop
		const d = Math.sqrt((x2-x1)*(x2-x1) + (y2-y1)*(y2-y1))
		const arrow_start_x = (x2-x1)*r1/d + x1 - editorContainer.offsetLeft + editorContent.scrollLeft
		const arrow_start_y = (y2-y1)*r1/d + y1 - editorContainer.offsetTop + editorContent.scrollTop
		const arrow_end_x = x2 - editorContainer.offsetLeft + editorContent.scrollLeft
		const arrow_end_y = y2 - editorContainer.offsetTop + editorContent.scrollTop
		const arrow = new LeaderLine(LeaderLine.pointAnchor(container, {x: arrow_start_x, y: arrow_start_y}), LeaderLine.pointAnchor(container, {x: arrow_end_x, y: arrow_end_y}))
		arrow.path = 'straight'  //将箭头的路径设置为直线
		// arrow.path = 'magnet'
		arrow.color = '#175ceb'
		arrow.size = 1
		arrow.endPlugSize = 2
		arrow.showEffectName = 'draw'
		return arrow
	}
}

export 	const createNewArrowTextMouse=(num_start: number, clientX: number, clientY: number, text: string, arrowNum: number, blocks: EditorBlockData[] | undefined, container: HTMLDivElement) => {
// 	const editorContent = document.getElementById('editor-content')
// 	const editorContainer = document.getElementById('editor-container')// eslint-disable-next-line @typescript-eslint/no-explicit-any
// 	if(editorContent && editorContainer){
// 		const LeaderLine: any = require("./plugins/leader-line.min.js")  //在不写对应的.d.ts文件的情况下，js文件不能通过es6的export/import导出引入，应该使用es5的module.exports和require导出引入
// 		const block_start :EditorBlockData = (blocks || [])[num_start]
// 		const r1 = (block_start.props.size || block_start.width) / 2
// 		const x1 = block_start.left + r1
// 		const y1 = block_start.top + r1
// 		const x2 = clientX - editorContainer.offsetLeft + editorContent.scrollLeft
// 		const y2 = clientY - editorContainer.offsetTop + editorContent.scrollTop
// 		const d = Math.sqrt((x2-x1)*(x2-x1) + (y2-y1)*(y2-y1))
// 		const arrow_start_x = (x2-x1)*r1/d + x1
// 		const arrow_start_y = (y2-y1)*r1/d + y1
// 		const arrow_end_x = x2
// 		const arrow_end_y = y2
		
// 		const div = document.createElement("div")
// 		div.id = 'arrowText' + arrowNum
// 		div.style.position = "absolute"
// 		div.style.zIndex = "2"  //string类型
// 		div.style.fontSize = "14px"
// 		div.style.color = "#828282"
// 		div.innerHTML = text
// 		editorContainer.appendChild(div)
// 		div.style.left = `${(arrow_start_x + arrow_end_x)/2 - div.clientWidth/2}px`
// 		div.style.top = `${(arrow_start_y + arrow_end_y)/2 - div.clientHeight/2}px`
// 		return div
// 	}
 }

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export function createEditorConfig() {

    const componentList: EditorComponent[] = []
    const componentMap: Record<string, EditorComponent> = {}

    return {
        componentList,
        componentMap,
        // eslint-disable-next-line @typescript-eslint/ban-types
        registry: <Props extends Record<string, EditorProps> = {}>(key: string, component: {
            label: string,
            preview: () => JSX.Element,
            // eslint-disable-next-line @typescript-eslint/no-explicit-any
            render: (data: { props: { [k in keyof Props]: any } }) => JSX.Element,
            props?: Props,
        }) => {
            // eslint-disable-next-line prefer-const
            let comp = { ...component, key }
            componentList.push(comp)
            componentMap[key] = comp
        }
    }

}

export type EditorConfig = ReturnType<typeof createEditorConfig>
