import { ref, watch } from "vue";

export function useModel<T>(getter: () => T, emitter: (val: T) => void) {
    
    const state= ref(getter()) as { value: T }
    // 这个变量是一个临时的响应式变量，是为了处理在某些组件中必须使用相应式的情况
    // 比如dialog服务中，输入框就必须使用响应式变量

    watch(getter, val => {
        if (val !== state.value) {
            state.value = val
        }
    })

    return {
        get value() {return state.value},
        set value (val:T) {
            if(state.value !== val){
                state.value =val
                emitter(val)
            }
        },
    }
}