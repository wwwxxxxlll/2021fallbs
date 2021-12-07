

document.getElementById("getcheck").addEventListener('click', function() {
	let email = document.getElementById("email").value;
    fn(email,568712);
});


let transporter = createTransport({
    host: 'smtp.qq.com',
    secure: true,
    auth: {
        user: '2314379811@qq.com',
        pass: 'ouirkqtzqvpoeaad' 
    }
});

module.exports = async function fn(email, code){
    let status = null
    await new Promise((resolve, reject) => {
        transporter.sendMail({
            from: '2314379811@qq.com',
            to: email, 
            subject: '网站账户注册验证码',
            html: `
            <p>网站账户注册验证码：</p>
        <span style="font-size: 18px; color: red">` + code + `</span>`

        }, function (err, info) {
            if (err) {
                status = 0
                reject()
            } else {
                status = 1
                resolve()
            }
        });
    })
    return status


}

