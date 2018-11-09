import axios from 'axios';

export default class Api {
    static myInstance = null;

    static getInstance() {
        if (Api.myInstance == null) {
            Api.myInstance = new Api();
        }
        return this.myInstance;
    };

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
