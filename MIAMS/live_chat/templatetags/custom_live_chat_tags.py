from django import template

register = template.Library()

@register.inclusion_tag('live_chat/partials/chat_bubble.html')
def render_chat():
    return {}