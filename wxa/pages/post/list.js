// pages/post/list.js
const app = getApp();
Page({

    /**
     * 页面的初始数据
     */
    data: {
        posts:null
    },

    /**
     * 生命周期函数--监听页面加载
     */
    onLoad: function (options) {
        let feedid = options.feedid;
        this.getPosts(feedid)
    },
    getPosts(fid){
        let _this = this;
        app.B.doing('正在加载...');
        app.B.callapi('posts',{feed_id:fid},(res)=>{
            if(res && res.data){
                _this.setData({
                    posts: res.data.posts
                })
            }
        })
    },
    gotoDetail(e){
        let post_id = e.currentTarget.dataset.id;
        wx.navigateTo({
            url: `/pages/post/detail?id=${post_id}`,
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