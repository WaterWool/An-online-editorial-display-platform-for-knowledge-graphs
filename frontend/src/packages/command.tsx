import { useCommander } from '@/packages/plugins/command.plugins'
import deepcopy from 'deepcopy';
import { EditorBlockData, EditorArrowData, EditorModelValue, EditorArrowList } from '@/packages/editor.utils';

export function useCommand(
    {
        blockFocusData,
		arrowFocusData,
        updateBlocks,
		updateArrows,
        dataModel,
        dragstart,
        dragend
    }: {
        blockFocusData: { value: { focus: EditorBlockData[], unfocus: EditorBlockData[] } },
		arrowFocusData: { value: { focus: EditorArrowList[], unfocus: EditorArrowList[] } },
        updateBlocks: (blocks?: EditorBlockData[]) => void,
		updateArrows: (arrows?: EditorArrowData[]) => void,
        dataModel: { value: EditorModelValue },
        dragstart: { on: (cb: () => void) => void, off: (cb: () => void) => void },
        dragend: { on: (cb: () => void) => void, off: (cb: () => void) => void },
    }
) {

    const commander = useCommander()

    commander.registry({
        name: 'delete',
        keyboard: ['backspace', 'delete', 'ctrl+d'],
        execute: () => {
            // eslint-disable-next-line prefer-const
            const blockData = {
                before: dataModel.value.blocks,
                after: blockFocusData.value.unfocus,
            }
			
			const arrowData = {
				before: dataModel.value.arrows,
				after: (() => {
					const arrowAf = deepcopy(dataModel.value.arrows)
					arrowFocusData.value.focus.forEach((arrowInformation: EditorArrowList, index1: number) => {
						let deleteIndex = -1
						!!arrowAf && arrowAf.forEach((arrowJson: EditorArrowData, index2: number) => {
							if (arrowJson.num_start === arrowInformation.num_start && arrowJson.num_end === arrowInformation.num_end) {
								deleteIndex = index2
							}
						})
						!!arrowAf && arrowAf.splice(deleteIndex, 1)
					})
					
					//删除对应的箭头
					const focusNum: number[] = []
					!!dataModel.value.blocks && dataModel.value.blocks.forEach((block: EditorBlockData, index: number) => block.focus && focusNum.push(index))
					const arrowAfter: EditorArrowData[] = []
					let saveArrow: boolean
					!!arrowAf && arrowAf.forEach((value1: EditorArrowData, index1: number) => {
						saveArrow = true
						focusNum.forEach((value2: number, index2: number) => {
							if(value1.num_start === value2 || value1.num_end === value2)
								saveArrow = false
						})
						if(saveArrow === true)
							arrowAfter.push(value1)
					})
					
					//更新箭头的起点和终点的序号
					const arrowAfterAfter = arrowAfter.map((value1: EditorArrowData, index1:number) => {
						return {
							num_start: (() => {
								let lessnum = 0
								focusNum.forEach((value2: number, index2: number) => {
									if(value2 < value1.num_start)
										lessnum++
								})
								return value1.num_start - lessnum
							})(),
							num_end: (() => {
								let lessnum = 0
								focusNum.forEach((value2: number, index2: number) => {
									if(value2 < value1.num_end)
										lessnum++
								})
								return value1.num_end - lessnum
							})(),
							text: value1.text
						}
					})
					return arrowAfterAfter
				})(),
			}
            return {
                undo: () => {
                    updateBlocks(deepcopy(blockData.before))
					updateArrows(deepcopy(arrowData.before))
                },
                redo: () => {
                    updateBlocks(deepcopy(blockData.after))
					updateArrows(deepcopy(arrowData.after))
                },
            }
        }
    })

    commander.registry({
        name: 'drag',
        init() {
            this.blockData = { before: null as null | EditorBlockData[], }
			this.arrowData = { before: null as null | EditorArrowData[], }
            const handler = {
                dragstart: () => {
					this.blockData.before = deepcopy(dataModel.value.blocks)
					this.arrowData.before = deepcopy(dataModel.value.arrows)
				},
                dragend: () => commander.state.commands.drag()
            }
            dragstart.on(handler.dragstart)
            dragend.on(handler.dragend)
            return () => {
                dragstart.off(handler.dragstart)
                dragend.off(handler.dragend)
            }
        },
        execute() {
            const beforeBlock = this.blockData.before //let
			const beforeArrow = this.arrowData.before
            const afterBlock = deepcopy(dataModel.value.blocks) //let
			const afterArrow = deepcopy(dataModel.value.arrows)
            return {
                undo: () => {
                    updateBlocks(deepcopy(beforeBlock))
					updateArrows(deepcopy(beforeArrow))
                },
                redo: () => {
                    updateBlocks(deepcopy(afterBlock))
					updateArrows(deepcopy(afterArrow))
                }
            }
        }
    })

    commander.registry({
        name: 'clear',
        execute: () => {
            // eslint-disable-next-line prefer-const
            let blockData = {
                before: deepcopy(dataModel.value.blocks),
                after: deepcopy([])
            }
			const arrowData = {
				before: deepcopy(dataModel.value.arrows),
				after: deepcopy([])
			}
            return {
                redo: () => {
                    updateBlocks(deepcopy(blockData.after))
					updateArrows(deepcopy(arrowData.after))
                },
                undo: () => {
                    updateBlocks(deepcopy(blockData.before))
					updateArrows(deepcopy(arrowData.before))
                }
            }

        }
    })

    commander.registry({
        name: 'placeTop',
        keyboard: 'ctrl+up',
        execute: () => {
            const data = {
                before: deepcopy(dataModel.value.blocks),
                after: deepcopy((() => {
                    const { focus, unfocus } = blockFocusData.value
                    const maxZIndex = unfocus.reduce((prev, block) => Math.max(prev, block.zIndex), -Infinity) + 1
                    focus.forEach(block => block.zIndex = maxZIndex)
                    return deepcopy(dataModel.value.blocks)
                })()),
            }
            return {
                redo: () => {
                    updateBlocks(deepcopy(data.after))
                },
                undo: () => {
                    updateBlocks(deepcopy(data.before))
                }
            }
        }
    })

    commander.registry({
        name: 'placeBottom',
        keyboard: 'ctrl+down',
        execute: () => {
            const data = {
                before: deepcopy(dataModel.value.blocks),
                after: deepcopy((() => {
                    const { focus, unfocus } = blockFocusData.value
                    let minZIndex = unfocus.reduce((prev, block) => Math.min(prev, block.zIndex), Infinity) - 1
                    if (minZIndex < 0) {
                        const dur = Math.abs(minZIndex)
                        unfocus.forEach(block => block.zIndex += dur)
                        minZIndex = 0
                    }
                    focus.forEach(block => block.zIndex = minZIndex)
                    return deepcopy(dataModel.value.blocks)
                })()),
            }
            return {
                redo: () => {
                    updateBlocks(deepcopy(data.after))
                },
                undo: () => {
                    updateBlocks(deepcopy(data.before))
                }
            }
        }
    })

    commander.registry({
        name: "updateBlock",
        execute: (newBlock: EditorBlockData, oldBlock: EditorBlockData) => {
            let blocks = deepcopy(dataModel.value.blocks || [])
            // eslint-disable-next-line
            let data = {
                before: blocks,
                after: (() => {
                    blocks = [...blocks]
                    const index = dataModel.value.blocks!.indexOf(oldBlock)
                    if (index > -1) {
                        blocks.splice(index, 1, newBlock)
                    }
                    return deepcopy(blocks)
                })(),
            }
            return {
                redo: () => {
                    updateBlocks(deepcopy(data.after))
                },
                undo: () => {
                    updateBlocks(deepcopy(data.before))
                },
            }
        }
    })

    commander.registry({
        name: "updateModelValue",
        execute: ( val: EditorModelValue ) => {
            // eslint-disable-next-line
            let data = {
                before: deepcopy(dataModel.value),
                after: deepcopy(val),
            }
            return {
                redo: () => {
                    dataModel.value = data.after
                },
                undo: () => {
                    dataModel.value = data.before
                },
            }
        }
    })

    commander.registry({
        name: 'selectAll',
        followQueue: false,
        keyboard: 'ctrl+a',
        execute: () => {
            return {
                redo: () => {
                    (dataModel.value.blocks || []).forEach(block => block.focus = true)
                },
            }
        },
    })

    commander.init()


    return {
        undo: () => commander.state.commands.undo(),
        redo: () => commander.state.commands.redo(),
        delete: () => commander.state.commands.delete(),
        clear: () => commander.state.commands.clear(),
        placeTop: () => commander.state.commands.placeTop(),
        placeBottom: () => commander.state.commands.placeBottom(),
        updateBlock: (newBlock: EditorBlockData, oldBlock: EditorBlockData) => commander.state.commands.updateBlock(newBlock, oldBlock),
        updateModelValue: (val: EditorModelValue) =>commander.state.commands.updateModelValue(val),
    }
}