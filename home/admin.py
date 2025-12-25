# home/admin.py - UPDATED VERSION
from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Question, QuizAttempt


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'category', 'question_text', 'correct_option')
    list_filter = ('category', 'correct_option')
    search_fields = ('question_text',)
    raw_id_fields = ('category',)


@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'category',
        'score_display',
        'percentage',
        'security_status',
        'tab_switches',
        'fullscreen_exits',
        'timestamp'
    )
    list_filter = ('is_flagged', 'category', 'timestamp')
    search_fields = ('user__username', 'user__email', 'category__name')
    readonly_fields = ('timestamp', 'security_summary')
    
    fieldsets = (
        ('Quiz Information', {
            'fields': ('user', 'category', 'score', 'total', 'timestamp')
        }),
        ('Security Monitoring', {
            'fields': ('tab_switches', 'fullscreen_exits', 'is_flagged', 'security_summary'),
            'classes': ('collapse',)
        }),
    )
    
    def score_display(self, obj):
        return f"{obj.score}/{obj.total}"
    score_display.short_description = 'Score'
    
    def percentage(self, obj):
        if obj.total > 0:
            percent = round((obj.score / obj.total) * 100, 1)
            color = 'green' if percent >= 70 else 'orange' if percent >= 50 else 'red'
            return format_html(
                '<span style="color: {}; font-weight: bold;">{:.1f}%</span>',
                color, percent
            )
        return '0%'
    percentage.short_description = 'Score %'
    
    def security_status(self, obj):
        if obj.is_flagged:
            return format_html(
                '<span style="background-color: #fee; color: #c00; padding: 3px 8px; border-radius: 3px; font-weight: bold;">🚩 FLAGGED</span>'
            )
        elif obj.tab_switches > 0 or obj.fullscreen_exits > 0:
            return format_html(
                '<span style="background-color: #ffeaa7; color: #d63031; padding: 3px 8px; border-radius: 3px;">⚠️ WARNING</span>'
            )
        return format_html(
            '<span style="background-color: #dfe; color: #0a0; padding: 3px 8px; border-radius: 3px;">✓ CLEAN</span>'
        )
    security_status.short_description = 'Status'
    
    def security_summary(self, obj):
        violations = []
        if obj.tab_switches > 0:
            violations.append(f"• {obj.tab_switches} tab switch(es)")
        if obj.fullscreen_exits > 0:
            violations.append(f"• {obj.fullscreen_exits} fullscreen exit(s)")
        
        if violations:
            return format_html(
                '<div style="padding: 10px; background: #fee; border-left: 4px solid #c00;">'
                '<strong style="color: #c00;">⚠️ Security Violations Detected:</strong><br>{}</div>',
                '<br>'.join(violations)
            )
        return format_html(
            '<div style="padding: 10px; background: #dfe; border-left: 4px solid #0a0;">'
            '<strong style="color: #0a0;">✓ No violations detected</strong></div>'
        )
    security_summary.short_description = 'Security Summary'
    
    actions = ['flag_attempts', 'unflag_attempts']
    
    def flag_attempts(self, request, queryset):
        updated = queryset.update(is_flagged=True)
        self.message_user(request, f'{updated} attempt(s) flagged successfully.')
    flag_attempts.short_description = "🚩 Flag selected attempts"
    
    def unflag_attempts(self, request, queryset):
        updated = queryset.update(is_flagged=False)
        self.message_user(request, f'{updated} attempt(s) unflagged successfully.')
    unflag_attempts.short_description = "✓ Unflag selected attempts"