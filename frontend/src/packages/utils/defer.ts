interface Defer {
    (): {
        resolve: () => void,
        reject: () => void,
        promise: Promise<void>
    },

    <T>(): {
        resolve: (val: T) => void,
        reject: () => void,
        promise: Promise<T>
    }
}

export const defer: Defer = () => {
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    const dfd = {} as any
    dfd.promise = new Promise((resolve, reject) => {
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        dfd.resolve = resolve as any
        dfd.reject = reject
    })
    return dfd
}