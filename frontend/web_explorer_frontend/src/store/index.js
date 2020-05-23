import vue from 'vue'
import vuex from 'vuex'

vue.use(vuex)

const store = new vuex.Store({
  state:{
    cascade_dir:[]
  },
  mutations:{
    change_cascade(state,target_data){
      state.cascade_dir = []
      state.cascade_dir.push(...target_data)
      console.log(state)
    }
  }
})

export default store
