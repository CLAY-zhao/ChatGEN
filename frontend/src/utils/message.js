import { ElMessage, ElNotification } from 'element-plus'


export function success_msg(msg) {
  ElMessage.success(msg)
}

export function error_msg(msg) {
  ElMessage.error(msg)
}

export function warning_msg(msg) {
  ElMessage.warning(msg)
}

export function notify_success(msg) {
  ElNotification({
    title: 'Success',
    message: msg,
    type: 'success'
  })
}

export function notify_warning(msg) {
  ElNotification({
    title: 'Warning',
    message: msg,
    type: 'warning'
  })
}

export function notify_info(msg) {
  ElNotification({
    title: 'Info',
    message: msg,
    type: 'info'
  })
}

export function notify_error(msg) {
  ElNotification({
    title: 'Error',
    message: msg,
    type: 'error'
  })
}

