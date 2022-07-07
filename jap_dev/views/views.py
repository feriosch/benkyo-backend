from jap_dev.views.kanji.main import MainKanjiView
from jap_dev.views.kanji.search import SearchKanjiView
from jap_dev.views.kanji.verify import VerifyKanjiView
from jap_dev.views.kanji.components import KanjiComponentsView
from jap_dev.views.word.main import WordMainView
from jap_dev.views.word.search import WordSearchView
from jap_dev.views.word.level import WordLevelView
from jap_dev.views.word.csv import WordCsvView
from jap_dev.views.collection.main import MainCollectionView
from jap_dev.views.user.main import MainUserView
from jap_dev.views.user.login import UserLoginView
from jap_dev.views.user.session import UserSessionView
from jap_dev.views.clause.main import ClauseMainView

views = {
    'kanji': {
        'main': MainKanjiView.as_view('kanji'),
        'search': SearchKanjiView.as_view('kanji_search'),
        'verify': VerifyKanjiView.as_view('kanji_verify'),
        'components': KanjiComponentsView.as_view('kanji_components')
    },
    'word': {
        'main': WordMainView.as_view('word'),
        'search': WordSearchView.as_view('word_search'),
        'level': WordLevelView.as_view('word_level'),
        'csv': WordCsvView.as_view('word_csv')
    },
    'collection': {
        'main': MainCollectionView.as_view('collection')
    },
    'user': {
        'main': MainUserView.as_view('user'),
        'login': UserLoginView.as_view('user_login'),
        'session': UserSessionView.as_view('user_session')
    },
    'clause': {
        'main': ClauseMainView.as_view('clause')
    }
}
