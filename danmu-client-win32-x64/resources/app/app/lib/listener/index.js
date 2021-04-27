'use strict'
// const packageJson = require('../../package.json')
// const player = require('../danmu/index')
// const Socket = require('socket.io-client')
const coordinator = require('electron').remote.getGlobal('coordinator')
const mysql = require('mysql')
const config = global.config
const async = require('async')
// let io
// let serverRandomNumber = null
module.exports = {
  init: function () {
    // io = Socket(config.socket.url)
    // io.heartbeatTimeout = config.socket.heartbeat
    // realInit(config)
    tryConnect()
  }
}

let intervalHandle
let con
let isRun = false

function tryConnect () {
  con = mysql.createConnection({
    host: config.mysql.host,
    user: config.mysql.user,
    password: config.mysql.password,
    database: config.mysql.database
  })
  con.connect(err => {
    if (err) {
      console.log('连接服务器 ' + config.host + ' 失败！' + err)
      setTimeout(tryConnect, 1000)
    } else {
      console.log('成功连接至数据库')
      intervalHandle = setInterval(fetchDanmu, config.mysql.fetchInterval)
    }
  })
}

function fetchDanmu () {
  if (isRun) {
    return
  }
  isRun = true
  con.query('SELECT id,content FROM wewall_msg WHERE danmu=0' + (config.mysql.censorship ? ' AND checked=1' : ''), (err, res) => {
    if (err) {
      clearInterval(intervalHandle)
      intervalHandle = undefined
      setTimeout(tryConnect, 0)
      console.log('数据库断线 ' + err)
      isRun = false
    } else {
      if (res.length === 0) {
        console.log('没有新的弹幕')
        isRun = false
        return
      }
      async.parallel(res.map(x => function (callback) {
        con.query('UPDATE wewall_msg SET danmu=1 WHERE id=?', [x.id], callback)
      }), (e, r) => {
        // console.log(e.length + ' ' + r.length)
        // console.log('res.length: ' + res.length)
        let converted = res.map(x => ({
          text: x.content,
          id: x.id
        }))
        console.log('得到了' + converted.length + '条弹幕')
        coordinator.emit('gotDanmu', converted)
        isRun = false
      })
    }
  })
}

/*
 function realInit () {
 let initCount = 0
 io.on('init', () => {
 initCount++
 io.emit('password', {
 password: config.socket.password,
 room: config.socket.room,
 info: {
 version: packageJson.version
 }
 })
 if (initCount > 1) {
 window.console.log('连接密码错误')
 }
 })
 io.on('connected', data => {
 initCount = 0
 window.console.log('已连接上弹幕服务器（' + data.version + '）')
 if (serverRandomNumber !== data.randomNumber) {
 if (serverRandomNumber !== null) {
 window.console.log('服务器似乎已重启，将清空弹幕池。')
 // 如果断线（服务器重启？）了，必须清理原有弹幕，否则会导致ID池不匹配
 }
 player.stop()
 player.clear()
 player.start()
 serverRandomNumber = data.randomNumber
 }
 })
 io.on('disconnect', () => {
 window.console.warn('与服务器的连接中断')
 })
 io.on('danmu', data => {
 window.console.log('得到' + data.data.length + '条弹幕')
 coordinator.emit('gotDanmu', data.data)
 })
 io.on('delete', data => {
 window.console.log('删除' + data.ids.length + '条弹幕')
 coordinator.emit('deleteDanmu', data)
 })
 }
 */
