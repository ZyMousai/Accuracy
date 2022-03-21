import store from '@/store/index.js';

function OperationVerification() {
    const roles = store.getters['account/roles']
    let ispass = null
    if (roles[0].id !== 1) {
        ispass = true
    } else {
        ispass = false
    }
    return ispass
}

export { OperationVerification }