import { Config } from './config.js';
import {gen_uuid} from '../utils/util.js';
let B = {
    toast:(title, icon) => {
        wx.showToast({
            title: title || '',
            mask: true,
            icon: icon || 'success'
        })
    },
    confirm: (title, content, cbk, showCancel = true) => {
        wx.showModal({
            title: title || '提示',
            content: content || '',
            showCancel: showCancel,
            success: (res) => {
                cbk && cbk(res);
            }
        })
    },
    msg: (title, content, cbk) => {
        B.confirm(title, content, cbk, false)
    },
    doing: (title) => {
        wx.showLoading({
            title: title || '正在加载...',
        })
    },
    done: () => {
        wx.hideLoading();
    },
    uuid: ()=>{
        let sessionid = wx.getStorageSync('sessionid') || '';
        return sessionid
    },
    callapi: (apiname, params, cbk) => {
        wx.request({
            url: `${Config.server}/api/${apiname}`,
            data: params,
            header: {
                'content-type': 'application/json', // 默认值
                'Cookie': `sessionid=${B.uuid()}`
            },
            success: (res) => {
                B.done();
                switch (res.data.code) {
                    case 0:
                        cbk && cbk(res.data)
                        break;
                    case -1:    
                        B.msg(res.data)
                        break;
                    default:
                        B.msg(res.data)
                        break;
                }
            },
            fail: (e) => {
                B.done();
                B.msg(e.errMsg);
            }
        })
    }
}

export {B}