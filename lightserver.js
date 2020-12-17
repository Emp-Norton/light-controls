const express = require('express');
const g = require('onoff').Gpio
const app = express();
const lamp = new g(16, 'out');

const on = () => {
    lamp.writeSync(1);
}

const off = () => {
    lamp.writeSync(0);
}

app.get('/lights-on', (req, res) => {
    on();
    res.send(`bedroom ack'd: on`);
})
app.get('/lights-off', (req, res) => {
    off();
    res.send(`bedroom ack'd: off`);
})
app.listen(8080, ()=> {
    console.log('Listening on 8080');
})
