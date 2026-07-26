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
        # Reverse note is independent; defaults to the forward note when omitted/blank.
        reverse_note = data.get('reverseNote') or note

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
            'note': reverse_note
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

    def put(self, word_id, related_word_id):
        """Edit ONLY this side of a related-word edge.

        Unlike post(), this never touches the counterpart and never swaps tags —
        the note/type/tags are written verbatim on word_id's edge alone.
        """
        data = request.get_json()
        rel_type = data.get('type', 'related')
        note = data.get('note', '')
        tags = data.get('tags', [])

        update = {'$set': {'related.$.type': rel_type, 'related.$.note': note}}
        if tags:
            update['$set']['related.$.tags'] = tags
        else:
            update['$unset'] = {'related.$.tags': ''}

        result = words().update_one(
            {'_id': ObjectId(word_id), 'related.wordId': ObjectId(related_word_id)},
            update
        )
        if result.matched_count == 0:
            return make_response({'error': 'Relationship not found'}, 404)

        return make_response({'success': True, 'message': 'Relationship updated'}, 200)


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

    def put(self, word_id):
        """Edit a basic (text-only) related edge, identified by its word text."""
        data = request.get_json()
        word_text = data.get('word', '').strip()
        rel_type = data.get('type', 'related')
        note = data.get('note', '')
        tags = data.get('tags', [])
        if not word_text:
            return make_response({'error': 'word is required'}, 400)

        update = {'$set': {'related.$.type': rel_type, 'related.$.note': note}}
        if tags:
            update['$set']['related.$.tags'] = tags
        else:
            update['$unset'] = {'related.$.tags': ''}

        result = words().update_one(
            {'_id': ObjectId(word_id), 'related.word': word_text},
            update
        )
        if result.matched_count == 0:
            return make_response({'error': 'Basic relationship not found'}, 404)

        return make_response({'success': True, 'message': 'Basic relationship updated'}, 200)
