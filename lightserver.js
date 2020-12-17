const express = require('express');
const g = require('onoff').Gpio
const app = express();

const args = process.argv.slice(2);
const room = args[0]
const port = args[1]
const pin = args[2]
const lamp = new g(pin, 'out');


const on = () => {
    lamp.writeSync(1);
}

const off = () => {
    lamp.writeSync(0);
}

app.get('/lights-on', (req, res) => {
    on();
    res.send(`${room} lights ack'd: on`);
})
app.get('/lights-off', (req, res) => {
    off();
    res.send(`${room} lights ack'd: off`);
})
app.listen(port, ()=> {
    console.log(`Listening on ${port}`);
})
