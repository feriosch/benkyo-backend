from flask.views import MethodView
from flask import make_response, request
from bson.objectid import ObjectId

from jap_dev.helpers.authentication import validate_session
from jap_dev.information import words


TAG_SWAPS = {
    'formal': 'casual',
    'casual': 'formal',
    'spoken': 'written',
    'written': 'spoken',
}


class WordRelatedView(MethodView):
    decorators = [validate_session]

    def post(self, word_id):
        """Add a related word relationship (DB word with relatedWordId)"""
        data = request.get_json()
        
        related_word_id = data.get('relatedWordId')
        rel_type = data.get('type', 'related')
        tags = data.get('tags', [])
        note = data.get('note', '')
        
        if not related_word_id:
            return make_response({'error': 'relatedWordId is required'}, 400)
        
        related_word = words().find_one({'_id': ObjectId(related_word_id)})
        if not related_word:
            return make_response({'error': 'Related word not found'}, 404)
        
        relationship = {
            'wordId': ObjectId(related_word_id),
            'type': rel_type,
            'note': note
        }
        if tags:
            relationship['tags'] = tags
        
        words().update_one(
            {'_id': ObjectId(word_id)},
            {'$push': {'related': relationship}}
        )
        
        reverse_relationship = {
            'wordId': ObjectId(word_id),
            'type': rel_type,
            'note': note
        }
        if tags:
            reverse_relationship['tags'] = [TAG_SWAPS.get(t, t) for t in tags]
        
        words().update_one(
            {'_id': ObjectId(related_word_id)},
            {'$push': {'related': reverse_relationship}}
        )
        
        return make_response({'success': True, 'message': 'Relationship added'}, 201)

    def delete(self, word_id, related_word_id):
        """Remove a related word relationship (DB word)"""
        words().update_one(
            {'_id': ObjectId(word_id)},
            {'$pull': {'related': {'wordId': ObjectId(related_word_id)}}}
        )
        
        words().update_one(
            {'_id': ObjectId(related_word_id)},
            {'$pull': {'related': {'wordId': ObjectId(word_id)}}}
        )
        
        return make_response({'success': True, 'message': 'Relationship removed'}, 200)


class WordRelatedBasicView(MethodView):
    """Manage text-only related word entries (basic words not in the DB)"""
    decorators = [validate_session]

    def post(self, word_id):
        data = request.get_json()
        word_text = data.get('word', '').strip()
        rel_type = data.get('type', 'related')
        tags = data.get('tags', [])
        note = data.get('note', '')

        if not word_text:
            return make_response({'error': 'word is required'}, 400)

        existing = words().find_one({
            '_id': ObjectId(word_id),
            'related.word': word_text
        })
        if existing:
            return make_response({'error': 'Basic word already linked'}, 409)

        relationship = {
            'word': word_text,
            'type': rel_type,
            'note': note
        }
        if tags:
            relationship['tags'] = tags

        words().update_one(
            {'_id': ObjectId(word_id)},
            {'$push': {'related': relationship}}
        )

        return make_response({'success': True, 'message': 'Basic word added'}, 201)

    def delete(self, word_id):
        word_text = request.args.get('word', '').strip()
        if not word_text:
            return make_response({'error': 'word query param is required'}, 400)

        words().update_one(
            {'_id': ObjectId(word_id)},
            {'$pull': {'related': {'word': word_text, 'wordId': {'$exists': False}}}}
        )

        return make_response({'success': True, 'message': 'Basic word removed'}, 200)
