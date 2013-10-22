# TODO
## Add ip address to the submition form
## Add value to the session/cookie
## 
def index():
    db.feedback.question_id.readable  = False
    db.feedback.gathered_on.readable  = False
        
    form = SQLFORM(db.feedback,formstyle='bootstrap')
    form.vars.question_id = 1
    if form.process().accepted:
        form = DIV(T('Feedback posted correctly'), _class='alert alert-info')
        response.flash = T('Thanks for voting')
    return {'form':form}


def show():
    grid = SQLFORM.grid(db.feedback)
    return locals()
    
    
def stats():
    questions = db(db.question).select()
    for question in questions:
        question['total'] = db(db.feedback.question_id == question.id).count()
        question['total_pos'] = db((db.feedback.question_id == question.id) & (db.feedback.answer == True)).count()
        
    return {'questions':questions}
