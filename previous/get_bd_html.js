// import axios;

var axios = require('axios');
// var cheerio = require('cheerio');
// var Promise = require('bluebird');
// var Song = require('./models/song');

var songsUrl = "http://bobdylan.com/songs-played-live/";

console.log(axios.get(songsUrl));
