// pages/index/index.js
import {Config} from '../../base/config.js';
const app = getApp();
Page({

    /**
     * 页面的初始数据
     */
    data: {
        feeds:null,
        showNewFeed:false,
        search_results:null,
        search_input:''
    },

    onLoad: function (options) {
        this.login();
    },
    login(){
        let _this = this;
        app.wxlogin((code)=>{
            let params = {
                'appid': Config.appid,
                'appsecret': Config.appsecret,
                'code':code
            }
            app.B.doing('正在加载...')
            app.B.callapi('wxa_login',params,(res)=>{
                if(res && res.data){
                    _this.setData({
                        feeds: res.data.feeds
                    })
                    let sessionid = res.data.sessionid;
                    if(sessionid)
                        wx.setStorageSync('sessionid', sessionid)
                }
            })
        })
    },
    showAdd(){
        this.setData({
            showNewFeed:true
        })
    },
    addFeed(e){
        let data = e.detail.value;
        let url = data.url;
        let _this = this;
        this.setData({
            showNewFeed:false
        });
        app.B.doing('正在解析...');
        app.B.callapi('add_rss',{url:url},(res)=>{
            let feeds = this.data.feeds;
            feeds.push({
                id: res.data.id,
                title: res.data.title,
                subtitle: res.data.subtitle,
                url: res.data.url
            })
            _this.setData({
                feeds: feeds
            })
        })
    },
    gotoPosts(e){
        let feed_id = e.currentTarget.dataset.id;
        wx.navigateTo({
            url: `/pages/post/list?feedid=${feed_id}`,
        })
    },
    search(e){
        let kw = e.detail.value;
        if(!kw){
            this.setData({
                search_results: null
            })
            return;
        }
        let _this = this;
        app.B.doing('正在搜索...');
        app.B.callapi('search_rss',{kw:kw},(res)=>{
            if(res && res.data){
                _this.setData({
                    search_results:res.data
                })
            }
        })
    },
    addFeedFromSearch(e){
        let feed = e.currentTarget.dataset.item;
        let feeds = this.data.feeds;
        let ids = feeds.map((o)=>{
            return o.id
        })
        this.setData({
            search_results:null
        })
        if (ids.includes(feed.id)){
            app.B.toast('已经在列表中')
            return;
        }
        feeds.push(feed);
        this.setData({
            feeds:feeds
        })
        app.B.toast('添加成功')
    },
    closeSearch(){
        this.setData({
            search_results: null,
            search_input: ''
        })
    },
    hideNewFeed(){
        this.setData({
            showNewFeed:false
        })
    },
    /**
     * 页面相关事件处理函数--监听用户下拉动作
     */
    onPullDownRefresh: function () {

    },

    /**
     * 页面上拉触底事件的处理函数
     */
    onReachBottom: function () {

    },

    /**
     * 用户点击右上角分享
     */
    onShareAppMessage: function () {

    }
})