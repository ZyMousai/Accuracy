import store from '@/store/index.js';

function OperationVerification(operate) {
    const roles = store.getters['account/roles']
    let ispass = null
    if (roles[0].operation.indexOf(operate) === -1) {
        ispass = true
    } else {
        ispass = false
    }
    return ispass
}

export { OperationVerification }