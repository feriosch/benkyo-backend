from flask.views import MethodView
from flask import make_response, request
from bson.objectid import ObjectId

from jap_dev.helpers.authentication import validate_session
from jap_dev.information import words


class WordRelatedView(MethodView):
    decorators = [validate_session]

    def post(self, word_id):
        """Add a related word relationship"""
        data = request.get_json()
        
        related_word_id = data.get('relatedWordId')
        rel_type = data.get('type', 'related')
        tags = data.get('tags', [])
        note = data.get('note', '')
        
        if not related_word_id:
            return make_response({'error': 'relatedWordId is required'}, 400)
        
        # Validate the related word exists
        related_word = words().find_one({'_id': ObjectId(related_word_id)})
        if not related_word:
            return make_response({'error': 'Related word not found'}, 404)
        
        # Build the relationship object
        relationship = {
            'wordId': ObjectId(related_word_id),
            'type': rel_type,
            'note': note
        }
        if tags:
            relationship['tags'] = tags
        
        # Add the relationship to the source word
        words().update_one(
            {'_id': ObjectId(word_id)},
            {'$push': {'related': relationship}}
        )
        
        # Also add the reverse relationship to the related word
        reverse_relationship = {
            'wordId': ObjectId(word_id),
            'type': rel_type,
            'note': note
        }
        if tags:
            # For reverse, swap certain nuance tags (e.g., formal <-> casual)
            reverse_tags = []
            tag_swaps = {
                'formal': 'casual',
                'casual': 'formal',
                'spoken': 'written',
                'written': 'spoken',
            }
            for tag in tags:
                reverse_tags.append(tag_swaps.get(tag, tag))
            reverse_relationship['tags'] = reverse_tags
        
        words().update_one(
            {'_id': ObjectId(related_word_id)},
            {'$push': {'related': reverse_relationship}}
        )
        
        return make_response({'success': True, 'message': 'Relationship added'}, 201)

    def delete(self, word_id, related_word_id):
        """Remove a related word relationship"""
        # Remove from source word
        words().update_one(
            {'_id': ObjectId(word_id)},
            {'$pull': {'related': {'wordId': ObjectId(related_word_id)}}}
        )
        
        # Remove the reverse relationship
        words().update_one(
            {'_id': ObjectId(related_word_id)},
            {'$pull': {'related': {'wordId': ObjectId(word_id)}}}
        )
        
        return make_response({'success': True, 'message': 'Relationship removed'}, 200)
