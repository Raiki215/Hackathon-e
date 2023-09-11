document.addEventListener('DOMContentLoaded', function() {
    const push = document.getElementById('push_btn');
    const searchResult = document.getElementById('result')
    const confirm_btn = document.getElementById('confirm_btn')

    push.addEventListener('click', function() {
        const search = document.getElementById("mail").value;
        console.log(search);
        if (search){
            search_result(search)
        } else {
            console.log('何も入ってない')
        }
    })

    



    let invite_list = []

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
                    let tr = document.createElement('tr');
                    let td = document.createElement('td');
                    let button = document.createElement('button');
                    button.dataset.user_id = element.id
                    button.dataset.user_mail = element.email
                    td.textContent = element.email;
                    button.innerText = '招待する';
                    button.onclick = function(){
                        // await fetch('http://127.0.0.1:5000/', )
                        let user_id = this.dataset.user_id
                        let user_mail = this.dataset.user_mail
                        
                        //招待する人リストにクリックした人が存在するチェック
                        var found = invite_list.find(e => e.id === user_id);
                        //存在しなかったら招待リストに追加
                        if(found === undefined) {
                            invite_list.push({id:user_id, email:user_mail})
                            invite_member_list(invite_list)
                        }
                        
                    }
                    searchResult.appendChild(tr).appendChild(td).appendChild(button);
                });

            })
        }catch(error){
            console.log('エラー',error);
        }
    }


    confirm_btn.addEventListener('click', function(){
        console.log(confirm_btn)
        invite_member(invite_list)
    })
    




})
function invite_member_list(list){
    const invite_result = document.getElementById('invite_result')
    invite_result.innerHTML = ''
    for(user of list){
        let tr = document.createElement('tr');
        let td = document.createElement('td');
        let button = document.createElement('button');
        button.dataset.user_id = user.id
        button.dataset.user_mail = user.email
        td.textContent = user.email;
        button.innerText = '取り消し';
        button.onclick = function(){
            let user_id = this.dataset.user_id //押されたボタンのカスタムデータ属性を取得
            //listの中から押されたユーザーのIDのindex番号を取得する
            var index = list.findIndex(e => e.id === user_id);
            //指定されたindex番号をlistから削除する
            // delete list[index] 不完全
            list.splice(index,1)
            //招待listを再生成
            invite_member_list(list)
        }   
        invite_result.appendChild(tr).appendChild(td).appendChild(button);
    }

}

//確認ボタンが押された時の動作
//listを取得する
//python側にpostで送る
//python側にチームメンバー登録プログラムにfetchでjson形式のlistを送る



async function invite_member(list){
    try{
        await fetch('http://127.0.0.1:5000/team/invite_member', {
                method: "POST",   // HTTP-Methodを指定する！
                headers: {
                    'Content-Type': 'application/json'  //どういう形式のデータを渡すか
                },
                body: JSON.stringify({"invite_list":list})
    })
    .then(res => {
        return res.json()
    })
    } catch(error) {
        console.log('エラー',error)
    }
}