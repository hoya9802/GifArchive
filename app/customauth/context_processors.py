from .models import Profile, Subscriber

# request.user를 사용할때는 무조건 request.user.is_authenticated를 넣어서 로그인된 유저의 정보에서만 검색해야함
def profiles(request):
    if request.user.is_authenticated:
        check = len(Profile.objects.filter(user_id=request.user))
    else:
        check = None
    return {
        "profile_exists": check
    }

def subscribers(request):
    if request.user.is_authenticated:
        # 현재 로그인한 유저가 구독한 프로필 목록을 가져옴
        sub_list = Subscriber.objects.filter(current_user=request.user).select_related('following__user_id')
        # 구독한 프로필에 연결된 MyUser의 닉네임과 프로필 이미지를 가져옴
        sub_info = [
            {
                'nickname': subscriber.following.user_id.nick_name,
                'profile_image': subscriber.following.profile_image
            }
            for subscriber in sub_list
        ]

        return {
            "sub_list": sub_info  # 목록을 닉네임과 이미지 정보로 변경
        }
    return {}