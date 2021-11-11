const express = require('express');
const g = require('onoff').Gpio
const app = express();
const logger = require('tracer').colorConsole();

const args = process.argv.slice(2);
const room = args[0]
const port = args[1]
const pin = args[2]
const ip = args[3]

const lamp = new g(pin, 'out');

const log = (data) => {
    let d = new Date();
    let date = d.toLocaleDateString();
    let time = d.toLocaleTimeString();
    logger.info(`${room} lights for ${ip} went ${data} at ${time} on ${date}.\n`);
}

const on = () => {
    lamp.writeSync(1);
    log('on');
}

const off = () => {
    lamp.writeSync(0);
    log('off');
}

app.get('/on', (req, res) => {
    on();
    res.send(`${room} lights ack'd: on - IP: ${ip} - Pin #${pin}\n`);
})
app.get('/off', (req, res) => {
    off();
    res.send(`${room} lights ack'd: off - IP: ${ip} - Pin #${pin}\n`);
})
app.listen(port, ()=> {
    console.log(`Listening on ${port}`);
})
