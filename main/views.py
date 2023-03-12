from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth import login, logout, authenticate
from .models import UserOfFacility, CaseReport
from django.db.models import Q
from django.contrib.auth.models import User
from .forms import (
    SignupForm,
    LoginForm,
    UserUpdateForm,
    UserOfFacilityForm,
    CaseReportForm
)
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView
)

class OnlyYouMixin(UserPassesTestMixin):
    raise_exception = True

    def test_func(self):
        # 今ログインしてるユーザーのpkと、そのユーザー情報ページのpkが同じか、又はスーパーユーザーなら許可
        user = self.request.user
        return user.pk == self.kwargs['pk'] or user.is_superuser

# ユーザー新規登録
def signup_view(request):
    if request.method != 'POST': form = SignupForm()
    form = SignupForm(request.POST)

    if form.is_valid():
        form.save()

        # フォームからusername & password1を読み取る
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        # 新規登録成功でログイン
        user = authenticate(username=username, password=password)
        login(request, user)
        request.session['user_id'] = request.user.id

        messages.add_message(request, messages.SUCCESS, "アカウントが作成されました。")
        return redirect("index")

    return render(request, 'login/signup.html', {'form': form})

# アカウント情報編集
class UserUpdate(UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'account/update.html'
    
    def form_valid(self, form):
        form.save()
        messages.add_message(self.request, messages.SUCCESS, "更新しました。")
        return redirect("index")

    success_url = reverse_lazy('index')

# アカウント削除(退会)
class UserDelete(DeleteView):
    template_name = 'login/login.html'
    model = User
    success_url = reverse_lazy('login')

# ログイン
def login_view(request):
    if request.method != 'POST': form = LoginForm()
    form = LoginForm(request, data=request.POST)
    user = None

    if form.is_valid():
        user = form.get_user()

    if user:
        login(request, user)
        request.session['user_id'] = user.id
        return redirect("index")

    return render(request, 'login/login.html', {'form': form})

# ログアウト
def logout_view(request):
    logout(request)

    return redirect("login")

# 利用者 一覧
class Index(ListView):
    template_name = 'user/index.html'
    context_object_name = 'users'
    paginate_by = 10

    def get_queryset(self):
        name_query = self.request.GET.get('name')
        organization_query = self.request.GET.get('organization')
        group_query = self.request.GET.get('group')
        
        # 検索に一致するデータがない場合、エラーメッセージを表示
        def validSearch():
            if queryset.count() <= 0:
                messages.add_message(self.request, messages.ERROR, "検索に一致するデータがありません。")

        # ログインユーザーが登録したデータのみ絞り込み
        queryset = UserOfFacility.objects.filter(user_id=self.request.session['user_id'])

        # 検索ロジック
        # 利用者名に検索があった場合
        if name_query:
            queryset = queryset.filter(Q(name__icontains=name_query))
            validSearch()
        # 所属組織に検索があった場合
        elif organization_query:
            queryset = queryset.filter(Q(organization__icontains=organization_query))
            validSearch()
        # グループに検索があった場合
        elif group_query:
            queryset = queryset.filter(Q(group__icontains=group_query))
            validSearch()

        return queryset

# 利用者 新規登録
class Create(CreateView):
    template_name = "user/create.html"
    model = UserOfFacility
    form_class = UserOfFacilityForm
    
    def form_valid(self, form):
        post = form.save(commit=False)
        # UserOfFacility.user_idにUser.user_idを登録
        post.user_id = self.request.user.id
        post.save()
        messages.add_message(self.request, messages.SUCCESS, "登録しました。")
        return redirect("index")

    success_url = reverse_lazy('index')

# 利用者 更新
class Update(UpdateView):
    template_name = "user/update.html"
    model = UserOfFacility
    form_class = UserOfFacilityForm

    def form_valid(self, form):
        form.save()
        messages.add_message(self.request, messages.SUCCESS, "更新しました。")
        return redirect("index")

    success_url = reverse_lazy('index')

# 利用者 削除
class Delete(DeleteView):
    template_name = 'user/index.html'
    model = UserOfFacility
    success_url = reverse_lazy('index')

# 事例記録 一覧
class CaseReportIndex(ListView):
    template_name = 'casereport/index.html'
    context_object_name = 'casereports'
    paginate_by = 20

    def get_queryset(self):
        date_min = self.request.GET.get('date_min')
        date_max = self.request.GET.get('date_max')
        date_min_time = str(date_min) + str(' 00:00:00.000000')
        date_max_time = str(date_max) + str(' 23:59:59.999999')

        # 検索に一致するデータがない場合、エラーメッセージを表示
        def validSearch():
            if queryset.count() <= 0:
                messages.add_message(self.request, messages.ERROR, "検索に一致するデータがありません。")

        # ログインユーザーが登録したデータのみ絞り込み
        queryset = CaseReport.objects.filter(user_id=self.request.session['user_id'])
        
        # 検索ロジック
        if date_min and date_max:
            queryset = queryset.filter(occurrence_date__range=[date_min_time, date_max_time]).order_by('occurrence_date')
            validSearch()
        elif date_min:
            queryset = queryset.filter(occurrence_date__gte=date_min_time).order_by('occurrence_date')
            validSearch()
        elif date_max:
            queryset = queryset.filter(occurrence_date__lte=date_max_time).order_by('occurrence_date')
            validSearch()

        return queryset

# 事例記録 新規登録
class CaseReportCreate(CreateView):
    template_name = "casereport/create.html"
    model = CaseReport
    form_class = CaseReportForm

    # 利用者名ドロップダウンで登録した利用者を表示する
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['nameList'] = UserOfFacility.objects.filter(user_id=self.request.session['user_id'])
        return context

    def form_valid(self, form):
        post = form.save(commit=False)
        # UserOfFacility.user_idにUser.user_idを登録
        post.user_id = self.request.user.id
        post.name = self.request.POST["userName"]
        post.save()
        messages.add_message(self.request, messages.SUCCESS, "登録しました。")
        return redirect("caseReportIndex")

    success_url = reverse_lazy('caseReportIndex')

# 事例記録 更新
class CaseReportUpdate(UpdateView):
    template_name = "casereport/update.html"
    model = CaseReport
    form_class = CaseReportForm
    
    # 利用者名は編集できないようにコンテキストでデータを渡す
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['nameReadOnly'] = CaseReport.objects.get(id=self.kwargs['pk']).name
        return context
    
    def form_valid(self, form):
        form.save()
        messages.add_message(self.request, messages.SUCCESS, "更新しました。")
        return redirect("caseReportIndex")

    success_url = reverse_lazy('caseReportIndex')

# 事例記録 削除
class CaseReportDelete(DeleteView):
    template_name = 'casereport/index.html'
    model = CaseReport
    success_url = reverse_lazy('caseReportIndex')