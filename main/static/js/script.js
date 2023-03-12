// ユーザー削除ボタン押下時
function AccountDeleteConfirm() {
    $('.deleteAccount').click(function(){
        if(!confirm('今まで登録されたデータもすべて削除されます。本当に削除しますか？')){
            return false;
        }else{
            ('#accountDeleteForm').submit();
        }
    });
}

// 利用者削除ボタン押下時
function UserDeleteConfirm() {
    $('.deleteUser').click(function(){
        if(!confirm('本当に削除しますか？')){
            return false;
        }else{
            ('#deleteUserForm').submit();
        }
    });
}

// 事例記録削除ボタン押下時
function CaseReportDeleteConfirm() {
    $('.deleteCasereport').click(function(){
        if(!confirm('本当に削除しますか？')){
            return false;
        }else{
            ('#deleteCaseReportForm').submit();
        }
    });
}

$(document).ready(function() {
    AccountDeleteConfirm();
    UserDeleteConfirm();
    CaseReportDeleteConfirm();
});