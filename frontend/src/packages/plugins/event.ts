type SimplyListener = () => void


// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export function createEvent() {
    // eslint-disable-next-line prefer-const
    let listeners: SimplyListener[] = [] 
    return {
        on: (cb: SimplyListener) => {
            listeners.push(cb)
        },
        off: (cb: SimplyListener) => {
            const index = listeners.indexOf(cb)
            if (index > -1) listeners.splice(index, 1)
        },
        emit: () => {
            listeners.forEach(item => item())
        },
    }
}