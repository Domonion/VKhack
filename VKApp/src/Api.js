import axios from 'axios';
import connect from '@vkontakte/vkui-connect';

export default class Api {
    static myInstance = null;

    static getInstance() {
        if (Api.myInstance == null) {
            Api.myInstance = new Api();
        }
        return this.myInstance;
    };

    getAccessToken() {
        return new Promise(function (token, reject) {
            connect.subscribe((e) => {
                switch (e.detail.type) {
                    case 'VKWebAppAccessTokenReceived':
                        token(e.detail.data.accessToken);
                        break;
                    case 'VKWebAppAccessTokenFailed':
                        reject(e.detail.data);
                        break;
                    default:
                        console.log(e.detail.type);
                }
            });
            connect.send("VKWebAppGetAuthToken", {"app_id": 6746736, "scope": "notify,friends"});
        })
    }

    getTags() {
        return new Promise(function(resolve, reject) {
            let request = new XMLHttpRequest();
            request.open('GET', 'http://');
            request.onload = function() {
                if (request.status === 200) {
                    resolve(request.response);
                } else {
                    reject(Error(
                        'Произошла ошибка. Код ошибки:' + request.statusText
                    ));
                }
            };
            request.send();
        });
    };


}
