import { computed, defineComponent, onMounted, PropType, ref } from "vue";
import { EditorBlockData, EditorConfig } from "./editor.utils";

export const EditorBlock = defineComponent({
    props:{
        block:{type: Object as PropType<EditorBlockData>, required:true},
        config:{type:Object as PropType<EditorConfig>, required:true}
    },
    setup(props){

        const el = ref({} as HTMLDivElement)

        const classes = computed (()=>[
            'editor-block',
            {
                'editor-block-focus':props.block.focus,
            }
        ])

        const styles = computed (()=>({
            top: `${props.block.top}px`,
            left:`${props.block.left}px`,
            zIndex: props.block.zIndex,
        }))

        onMounted(()=>{
            //自动居中功能，组件drop时候中心落到鼠标尖尖的位置
            const block = props.block
            if( block.adjustPosition === true ) {
                const {offsetWidth, offsetHeight} = el.value
                block.left = block.left - offsetWidth /2
                block.top = block.top - offsetHeight /2
                block.props.size = offsetWidth
                block.adjustPosition = false
            }
        })

        
        return () =>{
            const component = props.config.componentMap[props.block.componentKey]
            const Render = component.render({
                props: props.block.props || {},
            });

            return (
                <div class={classes.value} style={styles.value} ref={el}>
                    {Render}
                </div>
            )
        }
    },
})