# coding: UTF-8
"""`main` is the top level module for your Flask application."""

# Import the Flask Framework
from flask import Flask,render_template,request,redirect
from solve import SolveRSA
import re
app = Flask(__name__)
# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.

def formatStudentNumber(stdN):
    result = re.sub(r'^0+','',stdN)
    return int(result)

def findM(stdN,p,q):
    n = p * q
    ans = stdN % (n-2) + 2

    if ans == 536:
        ans = 535

    return ans

def formatPower(a,b):
    """aのb乗をa^1-n乗までフォーマットして返す感じ。多分。"""
    resultAry = []
    resultStr = ''
    for i in range(1,b+1):
        resultAry.append('{a}^{i} = {res}'.format(a=str(a), i=str(i), res=str(a ** i)))

    for line in resultAry:
        resultStr += '{resAry}{n}'.format(resAry=line,n='\n') 

    return resultStr
    

@app.route('/')
def top():
    """Return a friendly HTTP greeting."""
    return render_template('top.html')

@app.route('/result',methods=['POST','GET'])
def result():
    if request.method == 'POST':
        """
        try:
            # print(request.form.get('p'))
            p = int(request.form.get('p'))
            q = int(request.form.get('q'))
            m = findM(formatStudentNumber(request.form.get('stdId')),p,q)
            srsa = SolveRSA(m,p,q)
            m_e = formatPower(m,srsa.e())
            c_d = formatPower(srsa.c(),srsa.d())
        except:
            return redirect('/')
        """
        p = int(request.form.get('p'))
        q = int(request.form.get('q'))
        m = findM(formatStudentNumber(request.form.get('stdId')),p,q)
        srsa = SolveRSA(m,p,q)
        m_e = formatPower(m,srsa.e())
        c_d = formatPower(srsa.c(),srsa.d())


        # return 'OK!!!'
        ary={'inputStudentId':request.form.get('stdId'),'m':m,'lamdaN':srsa.lamdaN(),'e':srsa.e(),'d':srsa.d(),'n':srsa.n(),'c':srsa.c(),'m_e':m_e,'c_d':c_d}
        return render_template('result.html',ary=ary)
    else:
        return redirect('/')
        # return 'いきなりアクセスしないでくれ～～'
@app.route('/uda')
def showUda():
    return render_template('uda.html')

@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'よんまるよんのっとふぁうんど', 404


@app.errorhandler(500)
def application_error(e):
    """Return a custom 500 error."""
    #return '500 InternalServerError-ごめん、なんかエラーだ。すまないが、課題は自分で解いてくれ。', 500
    return render_template('500.html'),500


if __name__ == "__main__":
    #app.run(debug=True,host='0.0.0.0')
    print(formatPower(2,5))
