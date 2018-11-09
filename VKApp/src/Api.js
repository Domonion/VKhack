export default class Api {
    static myInstance = null;

    static getInstance() {
        if (Api.myInstance == null) {
            Api.myInstance = new Api();
        }
        return this.myInstance;
    }

    
}
