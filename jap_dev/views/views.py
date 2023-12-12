from jap_dev.views.kanji.main import MainKanjiView
from jap_dev.views.kanji.search import SearchKanjiView
from jap_dev.views.kanji.verify import VerifyKanjiView
from jap_dev.views.kanji.csv import KanjiCsvView
from jap_dev.views.kanji.components.regular import KanjiRegularComponentsView
from jap_dev.views.kanji.components.irregular import KanjiIrregularComponentsView
from jap_dev.views.kanji.radicals import KanjiRadicalsView
from jap_dev.views.word.main import WordMainView
from jap_dev.views.word.search import WordSearchView
from jap_dev.views.word.csv.main import WordCsvMainView
from jap_dev.views.word.csv.jlpt import WordCsvJlptView
from jap_dev.views.collection.main import MainCollectionView
from jap_dev.views.collection.search import CollectionSearchView
from jap_dev.views.user.main import MainUserView
from jap_dev.views.user.login import UserLoginView
from jap_dev.views.user.session import UserSessionView
from jap_dev.views.clause.main import ClauseMainView
from jap_dev.views.clause.search import ClauseSearchView

views = {
    'kanji': {
        'main': MainKanjiView.as_view('kanji'),
        'search': SearchKanjiView.as_view('kanji_search'),
        'verify': VerifyKanjiView.as_view('kanji_verify'),
        'csv': KanjiCsvView.as_view('kanji_csv'),
        'components': {
            'regular': KanjiRegularComponentsView.as_view('kanji_regular_components'),
            'irregular': KanjiIrregularComponentsView.as_view('kanji_irregular_components'),
        },
        'radicals': KanjiRadicalsView.as_view('kanji_radicals')
    },
    'word': {
        'main': WordMainView.as_view('word'),
        'search': WordSearchView.as_view('word_search'),
        'csv': {
            'main': WordCsvMainView.as_view('word_csv'),
            'jlpt': WordCsvJlptView.as_view('word_csv_jlpt')
        }
    },
    'collection': {
        'main': MainCollectionView.as_view('collection'),
        'search': CollectionSearchView.as_view('collection_search')
    },
    'user': {
        'main': MainUserView.as_view('user'),
        'login': UserLoginView.as_view('user_login'),
        'session': UserSessionView.as_view('user_session')
    },
    'clause': {
        'main': ClauseMainView.as_view('clause'),
        'search': ClauseSearchView.as_view('clause_search')
    }
}
