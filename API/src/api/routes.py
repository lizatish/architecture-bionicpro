from random import randint, choice, sample

from fastapi import APIRouter, Depends

from auth.current_user import check_granted_user_role
from settings import get_settings

router = APIRouter()
conf = get_settings()


@router.get('/reports')
async def report_generation(granted_user: dict = Depends(check_granted_user_role)):
    names = ['Bob', 'Mike', 'Anna', 'Claire']
    skills = ['word', 'excel', 'python', 'c#', 'java']

    return {
        'Name      ': choice(names),
        'Wage      ': randint(20, 30) * 100,
        'Skills    ': sample(skills, 3),
        'Efficiency': randint(5, 10),
        'Energy    ': randint(5, 10)
    }
