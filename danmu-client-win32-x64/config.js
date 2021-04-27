({
  socket: {
    url: 'http://127.0.0.1:3000',
    password: '',
    room: 'unlimited',
    heartbeat: 3000
  },
  mysql: {
    host: '39.107.76.131',
    user: 'wewall2018',
    password: '!Ima#gine@2018$sTuFes',
    database: 'wewall2018',
    fetchInterval: 100,
    censorship: true
  },
  display: {
    comment: {
      prizeProbability: 0.2,
      animationStyle: 'scroll',
      fontStyle: 'normal bold 5em 微软雅黑',
      fontColor: 'rgb(255, 255, 255)',
      lifeTime: 480,
      height: 50,
      strokeColor: 'rgb(0,0,0)'
    },
    image: true,
    imageWidth: 48
  },
  image: {
    sample: `<img class="lineimg" src="./images/8.png"/>`,
    regex: /<\s*img\s+class="(.+?)"\s+src="(.+?)"\/>/ig,
    whitelist: [
      'https://www.baidu.com/img/bd_logo1.png',
      'http://www.baidu.com/img/bd_logo1.png',
    ]
  }
})
