import { computed, defineComponent, PropType, reactive, ref, onMounted } from "vue";
import { EditorBlock } from "./editor-block";
import "./editor.scss"
import { createNewBlock, createNewArrow, createNewArrowText, createNewArrowMouse, createNewArrowTextMouse, EditorBlockData, EditorArrowData, EditorComponent, EditorConfig, EditorMarkLines, EditorModelValue, EditorArrowList, EditorArrowMoveList } from "./editor.utils";
import { createEvent } from "./plugins/event";
import { useModel } from "./useModel";
import { useCommand } from "./command";
import { $$dialog } from "./utils/dialog-service";
import { ElMessageBox, ElNotification } from "element-plus";
import { $$dropdown, DropdownOption } from "./utils/dropdown-service";
import { EditorOperator } from "./editor-operator";
import html2canvas from "html2canvas";
import deepcopy from 'deepcopy';
export const defaultArrowText = "关系"  //类似于C语言的#define

export const arrowList = reactive([] as EditorArrowList[])  //数组的每个元素为 箭头、相应的起点结点的数组序号、终点结点的数组序号
export let expState = reactive({
    editing: false
})

export const Editor = defineComponent({
    props: {
        modelValue: { type: Object as PropType<EditorModelValue>, required: true },
        config: { type: Object as PropType<EditorConfig>, required: true }
    },
    emits: {
        'update:modelValue': (val?: EditorModelValue) => true,
    },
    setup(props, ctx) {

        const dataModel = useModel(() => props.modelValue, val => ctx.emit('update:modelValue', val))


        const containerRef = ref({} as HTMLDivElement)
        // console.log('dataModel',dataModel);

        const containerStyle = computed(() => ({
            height: `${dataModel.value.container.height}px`,
            width: `${dataModel.value.container.width}px`,
        }))

        //计算选中和未选中的block
        const blockFocusData = computed(() => {
            const focus: EditorBlockData[] = []
            const unfocus: EditorBlockData[] = [];
            (dataModel.value.blocks || []).forEach(block => (block.focus ? focus : unfocus).push(block))
            return {
                focus,  //此时选中的数据
                unfocus //此时未选中的数据
            }
        })

		const arrowFocusData = computed(() => {
            const focus: EditorArrowList[] = []
            const unfocus: EditorArrowList[] = [];
            (arrowList || []).forEach(arrow => (arrow.focus ? focus : unfocus).push(arrow))
            return {
                focus,  //此时选中的数据
                unfocus //此时未选中的数据
            }
        })

        const selectIndex = ref(-1)
        const state = reactive({
            selectBlock: computed(() => (dataModel.value.blocks || [])[selectIndex.value]),  //当前选中组件
            editing: false,
			addArrow: false
        })
		expState = state

        const calsses = computed(() => [
            'editor',
            {
                'editor-editing': state.editing,
            },
            {
                'editor-showing': !state.editing,
            }
        ])

        const dragstart = createEvent()

        const dragend = createEvent()

        // console.log(props.config);

        const methods = {
            blockClearFocus: (block?: EditorBlockData) => {
                let blocks = (dataModel.value.blocks || []);
                if (blocks.length === 0) return
                if (block) {
                    blocks = blocks.filter(item => item !== block)
                }
                blocks.forEach(block => block.focus = false)
            },
			arrowAddOneFocus: (arrowListNum: number) => {  //arrowList数组中该箭头focus由false改为true，修改该箭头样式由未点中变为点中，该箭头的文字变为输入框
				arrowList[arrowListNum].focus = true
				arrowList[arrowListNum].arrow.dash = {animation: true, len: 4 , gap: 4}
				
				const arrowTextDiv = document.getElementById('arrowText' + arrowList[arrowListNum].arrowNum)
				const arrowTextInputDiv = document.createElement("div")
				arrowTextInputDiv.id = 'arrowText' + arrowList[arrowListNum].arrowNum
				arrowTextInputDiv.style.position = "absolute"
				arrowTextInputDiv.style.zIndex = "9990"
                const cWidth = arrowTextDiv!.clientWidth + 12
                const cHeight = arrowTextDiv!.clientHeight + 6
				!!arrowTextDiv && (arrowTextInputDiv.innerHTML = `<input id=${'arrowTextInput' + arrowList[arrowListNum].arrowNum} type="text" class="label-editor" style="width: ${cWidth || 40}px; height: ${cHeight || 19}px;">`)  //40，20为箭头无文字时产生的输入框的宽高，与下两行的20，9.5对应，注意修改
				const editorContainer = document.getElementById('editor-container')
				!!editorContainer && editorContainer.appendChild(arrowTextInputDiv)
				!!arrowTextDiv && (arrowTextInputDiv.style.left = arrowTextDiv.clientWidth ? arrowTextDiv.style.left : Number(arrowTextDiv.style.left.slice(0,-2)) - 20 + "px")
				!!arrowTextDiv && (arrowTextInputDiv.style.top = arrowTextDiv.clientHeight ? arrowTextDiv.style.top : Number(arrowTextDiv.style.top.slice(0,-2)) - 9.5 + "px")
				const arrowTextInput = document.getElementById('arrowTextInput' + arrowList[arrowListNum].arrowNum) as HTMLInputElement
				if(arrowTextInput){
					setTimeout(() => {arrowTextInput.focus()}, 10)  //这里需要延时，不然的话会先arrowTextInput.focus()，后点击画布，从而导致出现了取消输入框焦点的问题
					arrowTextInput.value = arrowList[arrowListNum].text
				}
				!!arrowTextDiv && arrowTextDiv.remove()
			},
			arrowClearOneFocus: (arrowListNum: number) => {  //arrowList数组中该箭头focus由true改为false，修改该箭头样式由点中变为未点中，该箭头的输入框变为文字
				arrowList[arrowListNum].focus = false
				arrowList[arrowListNum].arrow.dash = ''
				
				const arrowTextInputDiv = document.getElementById(arrowList[arrowListNum].arrowTextId)
				const arrowTextInput = document.getElementById('arrowTextInput' + arrowList[arrowListNum].arrowNum) as HTMLInputElement
				!!arrowTextInput && (arrowList[arrowListNum].text = arrowTextInput.value)
				createNewArrowText({num_start: arrowList[arrowListNum].num_start, num_end: arrowList[arrowListNum].num_end, text: arrowList[arrowListNum].text}, arrowList[arrowListNum].arrowNum, dataModel.value.blocks, containerRef.value, methods.blockClearFocus, methods.arrowClearAllFocus)
				!!dataModel.value.arrows && dataModel.value.arrows.forEach((arrow: EditorArrowData, index: number) => {
					if(arrow.num_start === arrowList[arrowListNum].num_start && arrow.num_end === arrowList[arrowListNum].num_end)
						arrow.text = arrowList[arrowListNum].text
				})
				!!arrowTextInputDiv && arrowTextInputDiv.remove()
			},
			arrowClearAllFocus: () => {  //arrowList数组所有focus为true的改为false，所有选中的箭头的样式改为未选中，所有输入框变为文字
				arrowList.forEach((arrowInformation: EditorArrowList, index: number) => {
					if (arrowInformation.focus === true) {
						arrowInformation.focus = false
						arrowInformation.arrow.dash = ''
						
						const arrowTextInputDiv = document.getElementById(arrowInformation.arrowTextId)
						const arrowTextInput = document.getElementById('arrowTextInput' + arrowInformation.arrowNum) as HTMLInputElement
						!!arrowTextInput && (arrowInformation.text = arrowTextInput.value)
						createNewArrowText({num_start: arrowInformation.num_start, num_end: arrowInformation.num_end, text: arrowInformation.text}, arrowInformation.arrowNum, dataModel.value.blocks, containerRef.value, methods.blockClearFocus, methods.arrowClearAllFocus)
						!!dataModel.value.arrows && dataModel.value.arrows.forEach((arrow: EditorArrowData, index: number) => {
							if(arrow.num_start === arrowInformation.num_start && arrow.num_end === arrowInformation.num_end)
								arrow.text = arrowInformation.text
						})
						!!arrowTextInputDiv && arrowTextInputDiv.remove()
					}
				})
			},
            updateBlocks: (blocks?: EditorBlockData[]) => {
                dataModel.value = {
					...dataModel.value, blocks,
                }
            },
			appendArrowList: (arrows?: EditorArrowData[]) => {  //根据arrows产生箭头和箭头文字并更新arrowList数组
				const arrowDiv = document.getElementById('editor-arrow')
				!!arrows && (
					arrows.forEach((jsonArrow, _index) => {
						const arrow = createNewArrow(jsonArrow, dataModel.value.blocks, containerRef.value)
						const svgArrowList = Array.from(document.getElementsByClassName('leader-line'))
						svgArrowList[svgArrowList.length - 1].id = 'arrow' + arrowNum
						const arrowSvg = document.getElementById(svgArrowList[svgArrowList.length - 1].id)
						!!arrowDiv && !!arrowSvg && arrowDiv.appendChild(arrowSvg)
						
						const arrowTextDiv = createNewArrowText(jsonArrow, arrowNum, dataModel.value.blocks, containerRef.value, methods.blockClearFocus, methods.arrowClearAllFocus)
						
						arrowList.push({ 
							num_start: jsonArrow.num_start,
							num_end: jsonArrow.num_end,
							text: jsonArrow.text,
							arrow: arrow,
							arrowNum: arrowNum,
							arrowId: svgArrowList[svgArrowList.length - 1].id,
							arrowTextId: arrowTextDiv.id,
							removed: false,
							focus: false
						})
						arrowNum++
					})
				)
			},
			updateArrows: (arrows?: EditorArrowData[]) => {
				//删除旧箭头 和 箭头文字或输入框
				arrowList.forEach((value, index) => {
					if(value.removed === false){
						const arrowSvg = document.getElementById(`${value.arrowId}`)
						const arrowTextDiv = document.getElementById(`${value.arrowTextId}`)
						!!arrowSvg && arrowSvg.remove()
						!!arrowTextDiv && arrowTextDiv.remove()
						value.removed = true
					}
				})
				//清空数组
				arrowList.splice(0)
				dataModel.value = {
					...dataModel.value, arrows,
                }
				methods.appendArrowList(dataModel.value.arrows)
			},
            showBlockData: (block: EditorBlockData) => {
                $$dialog.textarea(JSON.stringify(block), '节点数据', { editReadonly: true })
            },
            importBlockData: async (block: EditorBlockData) => {
                const text = await $$dialog.textarea('', '请输入要修改的JSON数据')
                try {
                    const data = JSON.parse(text || '')
                    commander.updateBlock(data, block)
                    if (data) ElNotification.success({ message: '修改成功', duration: 3000, position: "bottom-right" })
                } catch (e) {
                    console.error(e)
                    ElMessageBox.alert('解析JSON时出错。', { type: "error" })
                    ElNotification.error({ message: '修改失败', duration: 3000, position: "bottom-right", })
                }
            },
            dataURLToBlob(dataurl: string) {//ie 图片转格式
                const arr = dataurl.split(','), mime = arr[0].match(/:(.*?);/)![1],
                bstr = atob(arr[1]) 
                let n = bstr.length
                const u8arr = new Uint8Array(n);
                while (n--) {
                    u8arr[n] = bstr.charCodeAt(n);
                }
                return new Blob([u8arr], {type: mime})
            },
            downloadResult(name: string) {
                const canvasID = document.getElementById('editor-container');
                const a = document.createElement('a');
                html2canvas(canvasID!,{allowTaint: true}).then(canvas => {
                    const dom = document.body.appendChild(canvas);
                    // dom.style.display = "none";
                    // a.style.display = "none";
                    document.body.removeChild(dom);
                    const blob = methods.dataURLToBlob(dom.toDataURL("image/png"));
                    a.setAttribute("href", URL.createObjectURL(blob));
                    a.setAttribute("download", name + ".png")
                    document.body.appendChild(a);
                    a.click();
                    URL.revokeObjectURL(blob.toString());
                    document.body.removeChild(a);
                });
            },
            printOut() {
                const name = 'KnowledgeGraph(1)'
                // 个人观察只是截取可见范围以及以下的区域，所以先将滚动条置顶
                document.documentElement.scrollTop = 0 // 其他
                methods.downloadResult(name)
            }
        }

        const menuDraggier = (() => {

            let component = null as null | EditorComponent

            const blockHandler = {
                dragstart: (e: DragEvent, current: EditorComponent) => {
                    containerRef.value.addEventListener('dragenter', containerHandler.dragenter)
                    containerRef.value.addEventListener('dragover', containerHandler.dragover)
                    containerRef.value.addEventListener('dragleave', containerHandler.dragleave)
                    containerRef.value.addEventListener('drop', containerHandler.drop)
                    component = current
                    dragstart.emit()
                },
                dragend: (e: DragEvent) => {
                    containerRef.value.removeEventListener('dragenter', containerHandler.dragenter)
                    containerRef.value.removeEventListener('dragover', containerHandler.dragover)
                    containerRef.value.removeEventListener('dragleave', containerHandler.dragleave)
                    containerRef.value.removeEventListener('drop', containerHandler.drop)
                    component = null
                },
            }

            const containerHandler = {
                dragenter: (e: DragEvent) => {
                    e.dataTransfer!.dropEffect = 'move'
                },
                dragleave: (e: DragEvent) => {
                    e.dataTransfer!.dropEffect = 'none'
                },
                dragover: (e: DragEvent) => {
                    e.preventDefault()
                },
                drop: (e: DragEvent) => {
                    if (!state.editing) {
                        ElNotification.error({ message: '请进入编辑模式以修改', duration: 3000, position: "bottom-right", })
                        return
                    }
                    const blocks = [...dataModel.value.blocks || []]
                    blocks.push(createNewBlock({ component: component!, top: e.offsetY, left: e.offsetX, }))
                    methods.updateBlocks(blocks)
                    dragend.emit()
                },
            }

            return blockHandler
        })();

        const focusHandler = (() => {
            return {
                container: {
                    onMousedown: (e: MouseEvent) => {
                        //e.preventDefault();
                        if (!state.editing) return
                        if (e.currentTarget !== e.target) {
                            return
                        }
						let onArrow = false
						let onArrowIndex = -1
						const lineDistance = 5  //lineDistance为箭头的点击范围的宽的一半
						const { clientX, clientY } = e
						const editorContent = document.getElementById('editor-content')
						const editorContainer = document.getElementById('editor-container')
						if (editorContent && editorContainer) {
							const x_mouse = clientX - editorContainer.offsetLeft + editorContent.scrollLeft
							const y_mouse = clientY - editorContainer.offsetTop + editorContent.scrollTop
							arrowList.forEach((arrowInformation: EditorArrowList, index: number) => {
								const block_start :EditorBlockData = (dataModel.value.blocks || [])[arrowInformation.num_start]
								const block_end :EditorBlockData = (dataModel.value.blocks || [])[arrowInformation.num_end]
								const r1 = (block_start.props.size || 80) / 2
								const r2 = (block_end.props.size || 80) / 2
								const x1 = block_start.left + r1
								const y1 = block_start.top + r1
								const x2 = block_end.left + r2
								const y2 = block_end.top + r2
								if (y1 === y2) {
									let x_min: number
									let x_max: number
									if (x1 < x2) {
										x_min = x1 + r1
										x_max = x2 - r2
									}
									else {
										x_min = x2 + r2
										x_max = x1 - r1
									}
									const y_min = y1 - lineDistance
									const y_max = y1 + lineDistance
									if (x_mouse >= x_min && x_mouse <= x_max && y_mouse >= y_min && y_mouse <= y_max) {
										onArrow = true
										onArrowIndex = index
									}
								}
								else if (x1 === x2) {
									const x_min = x1 - lineDistance
									const x_max = x1 + lineDistance
									let y_min: number
									let y_max: number
									if (y1 < y2) {
										y_min = y1 + r1
										y_max = y2 - r2
									}
									else {
										y_min = y2 + r2
										y_max = y1 - r1
									}
									if (x_mouse >= x_min && x_mouse <= x_max && y_mouse >= y_min && y_mouse <= y_max) {
										onArrow = true
										onArrowIndex = index
									}
								}
								else {
									const d = Math.sqrt((x2-x1)*(x2-x1) + (y2-y1)*(y2-y1))
									const x_start = (x2-x1)*r1/d + x1
									const y_start = (y2-y1)*r1/d + y1
									const x_end = x2 - (x2-x1)*r2/d
									const y_end = y2 - (y2-y1)*r2/d
									const k = (y2-y1)*1.0/(x2-x1)
									let x_min: number
									let y_min: number
									let x_max: number
									let y_max: number
									if (y1 < y2) {
										x_min = x_start
										y_min = y_start
										x_max = x_end
										y_max = y_end
									}
									else {
										x_min = x_end
										y_min = y_end
										x_max = x_start
										y_max = y_start
									}
									if (y_mouse >= (x_mouse-x_min)*(-1.0)/k + y_min && y_mouse <= (x_mouse-x_max)*(-1.0)/k + y_max && y_mouse >= k*x_mouse + y1 - k*x1 - Math.sqrt(k*k+1)*lineDistance && y_mouse <= k*x_mouse + y1 - k*x1 + Math.sqrt(k*k+1)*lineDistance) {
										onArrow = true
										onArrowIndex = index
									}
								}
							})
						}
						
						if (onArrow) {
							if (e.shiftKey && !state.addArrow) {  //添加箭头时禁用多选
								if (blockFocusData.value.focus.length + arrowFocusData.value.focus.length <= 1) {
									if (arrowList[onArrowIndex].focus === false) {
										methods.arrowAddOneFocus(onArrowIndex)
									}
								}
								else {
									if (arrowList[onArrowIndex].focus === false) {
										methods.arrowAddOneFocus(onArrowIndex)
									}
									else {
										methods.arrowClearOneFocus(onArrowIndex)
									}
								}
							}
							else {
								if (arrowList[onArrowIndex].focus === false) {
									methods.blockClearFocus()
									methods.arrowClearAllFocus()
									methods.arrowAddOneFocus(onArrowIndex)
								}
							}
						}
						else if (!e.shiftKey) {
                            methods.blockClearFocus()
							methods.arrowClearAllFocus()
                            selectIndex.value = -1
                        }
                    },
                },

                block: {
                    onMousedown: (e: MouseEvent, block: EditorBlockData, index: number) => {
                        // if (!state.editing) {
                        //     return
                        // }
                        if (e.shiftKey && !state.addArrow) {  //添加箭头时禁用多选
                            if (blockFocusData.value.focus.length + arrowFocusData.value.focus.length <= 1) {
                                block.focus = true
                            } else {
                                block.focus = !block.focus
                            }
                        } else {
                            if (!block.focus) {
                                block.focus = true
                                methods.blockClearFocus(block)
								methods.arrowClearAllFocus()
                            }
							else if (state.addArrow) {  //添加箭头时取消多选
								methods.blockClearFocus(block)
								methods.arrowClearAllFocus()
							}
                        }
                        selectIndex.value = index
						if(!state.addArrow)
							blockDraggier.mousedown(e, index)
						else
							blockAddArrow.mousedown(e, index)
                    }
                }
            }
        })();

        const blockDraggier = (() => {

            const mark = reactive({ // 辅助线参数
                x: null as null | number,
                y: null as null | number,
            })

            let dragState = { // 拖动时的状态初始值
                startX: 0,
                startY: 0,
                startLeft: 0,
                startTop: 0,
                startPos: [] as { left: number, top: number }[],
                dragging: false,
                markLines: {} as EditorMarkLines,
            }

			const arrowMoveList: EditorArrowMoveList[] = []  //移动某一个结点时对应的需要移动的箭头

            const mousedown = (e: MouseEvent, index: number) => { // 鼠标按下之后的事件
                dragState = {
                    startX: e.clientX,
                    startY: e.clientY,
                    startLeft: state.selectBlock!.left,
                    startTop: state.selectBlock!.top,
                    startPos: blockFocusData.value.focus.map(({ top, left }) => ({ top, left })),
                    dragging: false,
                    markLines: (() => {
                        const { focus, unfocus } = blockFocusData.value
                        const width = state.selectBlock.props.size!
                        const height = state.selectBlock.props.size!
                        const lines: EditorMarkLines = { x: [], y: [] };
                        [...unfocus, {
                            top: 0,
                            left: 0,
                            props: {
                                size: dataModel.value.container.width,
                            }
                        }].forEach(block => { //下面这些是辅助线们
                            const { top: t, left: l } = block
                            const w = block.props.size || 80 
                            const h = block.props.size || 80
                            lines.y.push({ top: t, showTop: t })
                            lines.y.push({ top: t + h, showTop: t + h })
                            lines.y.push({ top: t + h / 2 - height / 2, showTop: t + h / 2 })
                            lines.y.push({ top: t - height, showTop: t })
                            lines.y.push({ top: t + h - height, showTop: t + h })

                            lines.x.push({ left: 0, showLeft: 0 })
                            lines.x.push({ left: l, showLeft: l })
                            lines.x.push({ left: l + w, showLeft: l + w })
                            lines.x.push({ left: l + w / 2 - width / 2, showLeft: l + w / 2 })
                            lines.x.push({ left: l - width, showLeft: l })
                            lines.x.push({ left: l + w - width, showLeft: l + w })
                        })
                        return lines
                    })(),
                }
				
				arrowMoveList.splice(0)  //清空数组
				arrowList.forEach((value, index_move) => {
					if(value.num_start === index || value.num_end === index)
						arrowMoveList.push({...value, index_move})
				})
				
                document.addEventListener('mousemove', mousemove)
                document.addEventListener('mouseup', mouseup)
            }

            const mousemove = (e: MouseEvent) => { // 鼠标移动事件

                if (!state.editing) return

                if (!dragState.dragging) {
                    dragState.dragging = true
                    dragstart.emit()
                }
                let { clientX: moveX, clientY: moveY } = e
                const { startX, startY } = dragState

                // 按住shift只能竖直或水平移动功能，没有问题，但是可能有些多余。
                // 感觉没有必要增加这个功能。
                // if (e.shiftKey) {
                //     if (Math.abs(moveX-startX) > Math.abs(moveY-startY)) {
                //         moveX = startX
                //     } else {
                //         moveY = startY
                //     }
                // }

                const currentLeft = dragState.startLeft + moveX - startX
                const currentTop = dragState.startTop + moveY - startY
                const currentMark = {
                    x: null as null | number,
                    y: null as null | number,
                }

                for (let i = 0; i < dragState.markLines.y.length; i++) {
                    const { top, showTop } = dragState.markLines.y[i];
                    if (Math.abs(top - currentTop) < 5) {
                        moveY = top + startY - dragState.startTop
                        currentMark.y = showTop
                        break
                    }
                }

                for (let i = 0; i < dragState.markLines.x.length; i++) {
                    const { left, showLeft } = dragState.markLines.x[i];
                    if (Math.abs(left - currentLeft) < 5) {
                        moveX = left + startX - dragState.startLeft
                        currentMark.x = showLeft
                        break
                    }
                }

                mark.x = currentMark.x
                mark.y = currentMark.y

                const durX = moveX - startX
                const durY = moveY - startY

                blockFocusData.value.focus.forEach((block, index) => {//这一段有问题，节点的大小超过了container的宽度，节点被挂在边缘移不走了
                    if (block.top >= 0 && block.top <= dataModel.value.container.height - (block.props.size||80)) {
                        block.top = dragState.startPos[index].top + durY
                    } else {
                        if (block.top < 0) block.top = 0
                        if (block.top > dataModel.value.container.height - (block.props.size||80)) block.top = dataModel.value.container.height - (block.props.size||80)
                    }

                    if (block.left >= 0 && block.left <= dataModel.value.container.width -(block.props.size||80)) {
                        block.left = dragState.startPos[index].left + durX
                    } else {
                        if (block.left < 0) block.left = 0

                        // if (block.left > dataModel.value.container.width - block.width) block.width = dataModel.value.container.width - block.width
                    }
                })

				const arrowDiv = document.getElementById('editor-arrow')
				arrowMoveList.forEach((arrow_move, index) => {
					const oldArrowSvg = document.getElementById(`${arrow_move.arrowId}`)
					const oldArrowTextDiv = document.getElementById(`${arrow_move.arrowTextId}`)
					!!oldArrowSvg && oldArrowSvg.remove()
					!!oldArrowTextDiv && oldArrowTextDiv.remove()
					arrowList[arrow_move.index_move].removed = true  //标记箭头删过了
					
					arrow_move.arrow = createNewArrow({num_start: arrow_move.num_start, num_end: arrow_move.num_end, text: arrow_move.text}, dataModel.value.blocks, containerRef.value)
					const svgArrowList = Array.from(document.getElementsByClassName('leader-line'))
					svgArrowList[svgArrowList.length - 1].id = 'arrow' + arrowNum
					const newArrowSvg = document.getElementById(svgArrowList[svgArrowList.length - 1].id)
					!!arrowDiv && !!newArrowSvg && arrowDiv.appendChild(newArrowSvg)
					arrow_move.arrowId = svgArrowList[svgArrowList.length - 1].id
					
					const arrowTextDiv = createNewArrowText({num_start: arrow_move.num_start, num_end: arrow_move.num_end, text: arrow_move.text}, arrowNum, dataModel.value.blocks, containerRef.value, methods.blockClearFocus, methods.arrowClearAllFocus)
					arrow_move.arrowTextId = arrowTextDiv.id
					
					arrowNum++
				})
            }

            const mouseup = () => { // 鼠标抬起后的事件
				if (dragState.dragging) {
					arrowMoveList.forEach((arrow_move, index) => {  //删去arrowMoveList数组中的箭头
						const arrowSvg = document.getElementById(`${arrow_move.arrowId}`)
						const arrowTextDiv = document.getElementById(`${arrow_move.arrowTextId}`)
						!!arrowSvg && arrowSvg.remove()
						!!arrowTextDiv && arrowTextDiv.remove()
					})
				}
                document.removeEventListener('mousemove', mousemove)
                document.removeEventListener('mouseup', mouseup)
                mark.x = null
                mark.y = null
                if (dragState.dragging) {
                    dragend.emit()
                }
            }

            return { mark, mousedown }

        })();
		
		const blockAddArrow = (() => {
			let num_start: number
			const fun: {mouseenter: any, mouseleave: any}[] = []  //存储的是函数构成的对象
			
			const mousedown = (e: MouseEvent, index1: number) => { // 鼠标按下之后的事件
				//焦点
				num_start = index1
				fun.splice(0)  //清空数组  //这行一定要写
				Array.from(document.getElementsByClassName('editor-block')).forEach((block, index2) => {
					fun.push({
						mouseenter: () => {!!dataModel.value.blocks && (dataModel.value.blocks[index2].focus = true)},
						mouseleave: () => {!!dataModel.value.blocks && (dataModel.value.blocks[index2].focus = false)}
					})
					if(index2 !== num_start){
						block.addEventListener('mouseenter', fun[index2].mouseenter)
						block.addEventListener('mouseleave', fun[index2].mouseleave)
					}
				})
				
				//产生箭头
				const { clientX, clientY } = e
				const arrowDiv = document.getElementById('editor-arrow')
				const arrow = createNewArrowMouse(num_start, clientX, clientY, dataModel.value.blocks, containerRef.value)
				const svgArrowList = Array.from(document.getElementsByClassName('leader-line'))
				svgArrowList[svgArrowList.length - 1].id = 'arrow' + arrowNum  //这里arrowNum就不加1了
				const arrowSvg = document.getElementById(svgArrowList[svgArrowList.length - 1].id)
				!!arrowDiv && !!arrowSvg && arrowDiv.appendChild(arrowSvg)
				
				const arrowTextDiv = createNewArrowTextMouse(num_start, clientX, clientY, defaultArrowText, arrowNum, dataModel.value.blocks, containerRef.value)
				
				document.addEventListener('mousemove', mousemove)
				document.addEventListener('mouseup', mouseup)
			}
			
			const mousemove = (e: MouseEvent) => { // 鼠标移动之后的事件
				if (!state.editing) return
				
				//删除旧箭头
				const arrowSvg2 = document.getElementById('arrow' + arrowNum)
				const arrowTextDiv2 = document.getElementById('arrowText' + arrowNum)
				!!arrowSvg2 && arrowSvg2.remove()
				!!arrowTextDiv2 && arrowTextDiv2.remove()
				
				//产生新箭头
				const { clientX, clientY } = e
				const arrowDiv = document.getElementById('editor-arrow')
				const arrow = createNewArrowMouse(num_start, clientX, clientY, dataModel.value.blocks, containerRef.value)
				const svgArrowList = Array.from(document.getElementsByClassName('leader-line'))
				svgArrowList[svgArrowList.length - 1].id = 'arrow' + arrowNum  //这里arrowNum就不加1了
				const arrowSvg3 = document.getElementById(svgArrowList[svgArrowList.length - 1].id)
				!!arrowDiv && !!arrowSvg3 && arrowDiv.appendChild(arrowSvg3)
				
				const arrowTextDiv3 = createNewArrowTextMouse(num_start, clientX, clientY, defaultArrowText, arrowNum, dataModel.value.blocks, containerRef.value)
			}
			
			const mouseup = () => { // 鼠标抬起后的事件
				//删除旧箭头
				const arrowSvg = document.getElementById('arrow' + arrowNum)
				const arrowTextDiv = document.getElementById('arrowText' + arrowNum)
				!!arrowSvg && arrowSvg.remove()
				!!arrowTextDiv && arrowTextDiv.remove()
				
				//产生新箭头
				if(blockFocusData.value.focus.length === 2){
					let num_end = -1;  //此处分号不写会报错
					(dataModel.value.blocks || []).forEach((block: EditorBlockData, index: number) => {
						if(block.focus === true && index !== num_start)
							num_end = index
					})
					
					let repeated = false;  //此处分号不写会报错
					(dataModel.value.arrows || []).forEach((arrow: EditorArrowData, index: number) => {
						if(arrow.num_start === num_start && arrow.num_end === num_end)
							repeated = true
					})
					
					if(repeated === false){
						!!dataModel.value.arrows && dataModel.value.arrows.push({num_start, num_end, text: defaultArrowText})
						methods.appendArrowList(dataModel.value.arrows)
					}
					
					!!dataModel.value.blocks && (dataModel.value.blocks[num_start].focus = false)  //这行放这里，效果更好
					!!dataModel.value.blocks && (dataModel.value.blocks[num_end].focus = false)
				}
				
				Array.from(document.getElementsByClassName('editor-block')).forEach((block, index) => {
					if(index !== num_start){
						block.removeEventListener('mouseenter', fun[index].mouseenter)
						block.removeEventListener('mouseleave', fun[index].mouseleave)
					}
				})
				document.removeEventListener('mousemove', mousemove)
				document.removeEventListener('mouseup', mouseup)
			}
			
			return { mousedown }
		})();

		//滚动条移动时更新箭头  //这个还是需要加上，不然会有错误
		// onMounted(()=>{
		// 	const editorContent= document.getElementById("editor-content")
		// 	!!editorContent && editorContent.addEventListener("scroll", () => {methods.updateArrows(dataModel.value.arrows)})
		// })

        const handler = {
            onContextmenuBlock: (e: MouseEvent, block: EditorBlockData) => { //右键菜单的handler
                e.preventDefault()
                e.stopPropagation()

                $$dropdown({
                    reference: e,
                    content: () => (<>
                        <DropdownOption label="置顶" icon="icon-run-up" tip="Ctrl+Up"{...{ onClick: commander.placeTop }} />
                        <DropdownOption label="置底" icon="icon-run-in" tip="Ctrl+Down"{...{ onClick: commander.placeBottom }} />
                        <DropdownOption label="删除" icon="icon-delete" tip="Backspace"{...{ onClick: commander.delete }} />
                        <DropdownOption label="查看属性" icon="icon-code" tip=" "{...{ onClick: () => methods.showBlockData(block) }} />
                        <DropdownOption label="修改属性" icon="icon-edit" tip=" " {...{ onClick: () => methods.importBlockData(block) }} />
                    </>)
                })
            },
        }

        const commander = useCommand({
            blockFocusData,
			arrowFocusData,
            updateBlocks: methods.updateBlocks,
			updateArrows: methods.updateArrows,
            dataModel,
            dragstart,
            dragend,
        });

        const toolButtons = [ // 为了方便定义的一个工具栏按钮数组，用的时候直接遍历数组
            {
                label: () => state.editing ?  '查看': '编辑',
                icon: () => state.editing ?  'icon-layers': 'icon-edit',
                handler: () => {
                    if (!state.editing) {
                        methods.blockClearFocus()
                        ElNotification.info({ message: '进入编辑模式', duration: 3000, position: "bottom-right", })
                    } else {
						methods.arrowClearAllFocus()  //编辑模式进入查看模式时如果有点上的箭头要变回来
                        ElNotification.info({ message: '进入预览模式', duration: 3000, position: "bottom-right", })
                    }
                    if (state.addArrow) {
                        const arrayLength = Array.from(document.getElementsByClassName('editor-head-tools-button')).length - 1
                        const toolButtonAddArrow = Array.from(document.getElementsByClassName('editor-head-tools-button'))[arrayLength] as HTMLDivElement  //目前此按钮在数组的下标为10，注意修改
                        toolButtonAddArrow.style.backgroundColor = ''
                        toolButtonAddArrow.style.color = ''
                        state.addArrow = !state.addArrow
                    }
                    state.editing = !state.editing
                },
                tip: () => state.editing ? '点击进入查看模式' : '点击进入编辑模式',
            },
            {
                label: '撤销',
                icon: 'icon-direction-left',
                handler: () => { 
                    if(!state.editing) return
                    commander.undo()
                },
                tip: 'Ctrl+Z'
            },
            {
                label: '重做',
                icon: 'icon-direction-right',
                handler: () => { 
                    if(!state.editing) return
                    commander.redo()
                },
                tip: 'Ctrl+Y, Ctrl+Shift+Z'
            },
            {
                label: '导入',
                icon: 'icon-code',
                handler: async () => {
                    const text = await $$dialog.textarea('', '请在下方的输入框内粘贴导入内容(JSON)')
                    try {
                        const data = JSON.parse(text || '')
                        dataModel.value = data
                        if (data) ElNotification.success({ message: '导入成功', duration: 3000, position: "bottom-right" })
                    } catch (e) {
                        console.error(e)
                        ElMessageBox.alert('解析JSON时出错。请检查字符串是否有遗漏。', { type: "error" })
                        ElNotification.error({ message: '导入失败', duration: 3000, position: "bottom-right", })
                    }

                },
                tip: '导入JSON数据'
            },
            {
                label: '导出',
                icon: 'icon-shebeikaifa',
                handler: () => $$dialog.textarea(JSON.stringify(dataModel.value), '导出的JSON数据', { editReadonly: true }),
                tip: '导出JSON数据'
            },
            {
                label: '置顶',
                icon: 'icon-run-up',
                handler: () => { 
                    if(!state.editing) return
                    commander.placeTop()
                },
                tip: 'Ctrl+Up'
            },
            {
                label: '置底',
                icon: 'icon-run-in',
                handler: () => { 
                    if(!state.editing) return
                    commander.placeBottom()
                },
                tip: 'Ctrl+Down'
            },
            {
                label: '删除',
                icon: 'icon-ashbin',
                handler: () => { 
                    if(!state.editing) return
                    commander.delete()
                },
                tip: 'Ctrl+D, Backspace, Delete'
            },
            {
                label: '清空',
                icon: 'icon-error',
                handler: () => { 
                    if(!state.editing) return
                    commander.clear(),
                    ElNotification.warning({ message: '已清空画布上的内容', duration: 3000, position: "bottom-right", }) 
                }
            },
            // {
            //     label: '图片',
            //     icon: 'icon-xingzhuang-tupian',
            //     handler: methods.printOut,
            //     tip: '该功能还在开发阶段'
            // },
			{
				label: '关系',
				icon: 'icon-guizeyinqing',
				handler: () => {
                    if(state.editing){
                        state.addArrow = !state.addArrow
                        const arrayLength = Array.from(document.getElementsByClassName('editor-head-tools-button')).length - 1
                        const toolButtonAddArrow = Array.from(document.getElementsByClassName('editor-head-tools-button'))[arrayLength] as HTMLDivElement  //目前此按钮在数组的下标为10，注意修改
                        toolButtonAddArrow.style.backgroundColor = state.addArrow ? '#175ceb' : ''
                        toolButtonAddArrow.style.color = state.addArrow ? '#ffffff' : ''
                        toolButtonAddArrow.style.borderRadius = "0 0 5px 5px"
                        if(state.addArrow){
                            ElNotification.info({ message: '节点位置已锁定，可以尝试在节点间拖拽以添加边', duration: 3000, position: "bottom-right", })                         
                        } else {
                            ElNotification.info({ message: '节点位置已解锁', duration: 3000, position: "bottom-right", })
                        }
                        } else {
                        ElNotification.error({ message: '查看状态下不能添加关系', duration: 3000, position: "bottom-right", }) 
                    }
				},
                tip: () => state.editing ? '点击添加关系': '查看状态下不能添加关系',
			}
        ]
		
		let arrowNum = 1
		onMounted(()=>{
			methods.appendArrowList(dataModel.value.arrows)
		})

        return () => (
            <div class={calsses.value} id="editor">
                <div class="editor-menu">
                    {props.config.componentList.map(component => (
                        <div class="editor-menu-item"
                            draggable
                            onDragend={menuDraggier?.dragend}
                            onDragstart={(e) => menuDraggier?.dragstart(e, component)}>
                            <span class="editor-menu-item-label">{component.label}</span>
                            <div class="editor-menu-item-content">
                                {component.preview()}
                            </div>
                        </div>
                    ))}
                </div>
                <div class="editor-head">
                    <div class="editor-head-logo">EasyKG</div>
                    <div class="editor-head-tools">
                        {toolButtons.map((btn, index) => {
                            const label = typeof btn.label === "function" ? btn.label() : btn.label
                            const icon = typeof btn.icon === "function" ? btn.icon() : btn.icon
                            const tip = typeof btn.tip === "function" ? btn.tip() : btn.tip
                            const content = (<div key={index} class="editor-head-tools-button" onClick={btn.handler}>
                                <i class={`iconfont ${icon}`} />
                                <span>{label}</span>
                            </div>)
                            return !btn.tip ? content : <el-tooltip effect="light" content={tip} placement="bottom">{content}</el-tooltip>
                        })
                        }
                    </div>
                    <div class="editor-head-user">
                        <span><el-avatar src="https://uploadstatic.mihoyo.com/contentweb/20200828/2020082814015644368.png"></el-avatar></span>
                        <i class={`iconfont icon-setting`} />
                    </div>
                </div>
                <EditorOperator block={state.selectBlock} config={props.config} dataModel={dataModel} updateBlock={commander.updateBlock} updateModelValue={commander.updateModelValue} />
                <div class="editor-body" id="editor-body">
                    <div class="editor-content" id="editor-content">
                        <div class="editor-container" id="editor-container"
                            style={containerStyle.value}
                            ref={containerRef}
                            {...focusHandler.container}
                        >
                            {!!dataModel.value.blocks && (
                                dataModel.value.blocks.map((block, index) => (
                                    <EditorBlock config={props.config}
                                        block={block}
                                        key={index}
                                        {...{
                                            onMousedown: (e: MouseEvent) => focusHandler.block.onMousedown(e, block, index),
                                            onContextmenu: (e: MouseEvent) => handler.onContextmenuBlock(e, block)
                                        }}
                                    />
                                ))
                            )}
                            {blockDraggier.mark.y !== null && (
                                <div class="editor-markline-x" style={{ top: `${blockDraggier.mark.y}px` }} />
                            )}
                            {blockDraggier.mark.x !== null && (
                                <div class="editor-markline-y" style={{ left: `${blockDraggier.mark.x}px` }} />
                            )}
							<div class="editor-arrow" id="editor-arrow"></div>
                        </div>
                    </div>
                </div>
            </div>
        )
    }
})
