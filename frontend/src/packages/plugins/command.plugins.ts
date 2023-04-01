import { onUnmounted, reactive } from "vue"
import { KeyboardCode } from "./keyboard-code"

export interface CommandExecute {
    undo?: () => void,
    redo: () => void,
}

export interface Command {
    name: string,
    keyboard?: string | string[],
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    execute: (...args: any[]) => CommandExecute,
    followQueue?: boolean,
    init?: () => void,
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    blockData?: any,
	arrowData?: any,
}

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export function useCommander() {

    const state = reactive({
        current: -1,
        queue: [] as CommandExecute[],
        commandArray: [] as Command[],
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        commands: {} as Record<string, (...args: any[]) => void>,
        destroyList: [] as ((() => void) | undefined)[],
    })

    const registry = (command: Command) => {
        state.commandArray.push(command)
        state.commands[command.name] = (...args) => {
            const { undo, redo } = command.execute(...args)
            redo()
            if (command.followQueue === false) {
                return
            }
            // eslint-disable-next-line prefer-const
            let { queue, current } = state
            if (queue.length > 0) {
                queue = queue.slice(0, current + 1)
                state.queue = queue
            }
            queue.push({ undo, redo })
            state.current = current + 1;
        }
    }

    const KeyboardEvent = (() => {

        const onKeydown = (e: KeyboardEvent) => {
            if (document.activeElement !== document.body) {
                return;
            }
            // console.log(e);
            const { keyCode, shiftKey, altKey, ctrlKey, metaKey } = e
            // eslint-disable-next-line prefer-const
            let keyString: string[] = []
            if (ctrlKey || metaKey) keyString.push('ctrl')
            if (shiftKey) keyString.push('shift')
            if (altKey) keyString.push('alt')
            if (KeyboardCode[keyCode] !== 'shift' && KeyboardCode[keyCode] !== 'ctrl' && KeyboardCode[keyCode] !== 'alt') {
                keyString.push(KeyboardCode[keyCode])
            } else return                                   //此处判断可能有bug
            const keyNames = keyString.join('+')
            state.commandArray.forEach(({ keyboard, name }) => {
                if (!keyboard) { return }
                const keys = Array.isArray(keyboard) ? keyboard : [keyboard]
                if (keys.indexOf(keyNames) > -1) {
                    state.commands[name]()
                    e.stopPropagation()
                    e.preventDefault()
                }
            })

        }
        const init = () => {
            window.addEventListener('keydown', onKeydown)
            return () => window.removeEventListener('keydown', onKeydown)
        }
        return init

    })();

    const init = () => {
        const onKeydown = (e: KeyboardEvent) => {
            e
        }
        window.addEventListener('keydown', onKeydown)
        // eslint-disable-next-line @typescript-eslint/ban-ts-comment
        // @ts-ignore
        state.commandArray.forEach(command => !!command.init && state.destroyList.push(command.init())) //?不知道为什么不让用 init()只好先ignore了
        state.destroyList.push(KeyboardEvent())
        state.destroyList.push(() => { window.removeEventListener('keydown', onKeydown) })
    }

    registry({
        name: 'undo',
        keyboard: 'ctrl+z',
        followQueue: false,
        execute: () => {
            return {
                redo: () => {
                    if (state.current === -1) {
                        return
                    }
                    const queueItem = state.queue[state.current]
                    if (queueItem) {
                        !!queueItem.undo && queueItem.undo()
                        state.current--
                    }
                },
            }
        }
    })

    registry({
        name: 'redo',
        keyboard: ['ctrl+y', 'ctrl+shift+z'],
        followQueue: false,
        execute: () => {
            return {
                redo: () => {
                    const queueItem = state.queue[state.current + 1]
                    if (queueItem) {
                        queueItem.redo()
                        state.current++
                    }
                },
            }
        },
    })

    onUnmounted(() => {
        state.destroyList.forEach(fn => !!fn && fn())
    })

    return {
        state,
        registry,
        init
    }

}
