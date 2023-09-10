document.addEventListener('DOMContentLoaded', function() {
    const push = document.getElementById('push_btn');
    const searchResult = document.getElementById('result')
    async function search_result(search) {

        try{
            await fetch('http://127.0.0.1:5000/team/mail_search', {
                method: "POST"   // HTTP-Methodを指定する！
                // body: form        // リクエストボディーにフォームデータを設定
            })
            .then(res => {
                return res.json()
            })
            .then(json => {
                json.forEach(element => {
                    console.log(element)
                });
            })
        }catch(error){
            console.log('エラー',error);
        }
    }
    
    function displayResult(results) {
        // searchResult.innerHTML = ''
        // results.foreach(result=> {
            // const div = document.createElement('div');
            // div.textContent = result.name;
            // searchResult.appendChild(div)
        // })
        console.log(results)
    }
    
    

    push.addEventListener('click', function() {
        const search = document.getElementById("mail").value;
        search_result(search)
    })
    async function search_result(search) {

        try{
            await fetch('http://127.0.0.1:5000/team/mail_search', {
                method: "POST",   // HTTP-Methodを指定する！
                headers: {
                    'Content-Type': 'application/json'  //どういう形式のデータを渡すか
                },
                body: JSON.stringify({"word":search})
                // body: form        // リクエストボディーにフォームデータを設定
            })
            .then(res => {
                return res.json()
            })
            .then(json => {
                console.log(json)
                searchResult.innerHTML = ''
                json.forEach(element => {
                    let div = document.createElement('div');
                    div.textContent = element.email;
                    searchResult.appendChild(div)
                });

            })
        }catch(error){
            console.log('エラー',error);
        }
    }

})