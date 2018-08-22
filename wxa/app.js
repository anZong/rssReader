//app.js
import { B } from './base/base.js';
App({
    onLaunch: function () {

    },
    globalData: {
        userInfo: null
    },
    wxlogin(cbk){
        wx.login({
            success:(res)=>{
                cbk && cbk(res.code);
            }
        })
    },
    B:B
})