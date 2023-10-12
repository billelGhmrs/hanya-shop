from flask import Flask, render_template, request
from flask_mysqldb import MySQL
from dotenv import load_dotenv
import os


def new_section(list,section):
  result=True
  for i in list:
    if section == i[0]:
      result = False
  return result

def order_by_section(sections):
  l = len(sections)
  result=[]
  for i in range(l):
    if new_section(result,sections[i][0]):
      j = i
      products=[]
      for j in range(i,l):
        if sections[j][0] == sections[i][0]:
          products.append(sections[j][1])
      temp=[sections[i][0],products]
      result.append(temp)
 # print(result)

  
  return result

app = Flask(__name__)

load_dotenv()

# Access the variables
password = os.getenv("Hanya_Billel_password")

# MySQL configurations
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'Hanya_Billel'
app.config['MYSQL_PASSWORD'] = password
app.config['MYSQL_DB'] = 'myshop'  # Use your database name
mysql = MySQL(app)



@app.route('/')
def index():
    cur = mysql.connection.cursor()

    cur.execute("SELECT * FROM sections")

    sections= cur.fetchall()
    ordered_sections= order_by_section(sections)
    ordered_sections_with_products=[]

    for section in ordered_sections:
       section_name= section[0]
       section_products=section[1]
       temp=[]
       for id in section_products:
         cur.execute("SELECT product_id, name, price, descreption, qte, pictures FROM products WHERE product_id = %s", (id,))

         products = cur.fetchall()
         #products[5]=products[5].split(',')
         product=[products[0][0],products[0][1],products[0][2],products[0][3],products[0][4],products[0][5].split(',')]
         temp.append(product)
         
         #print(products[0][5].split(','))
         #print(products[0])
      
       #print(temp)
       ordered_sections_with_products.append([section_name,temp])

    #print(pictures)
    cur.execute("SELECT * FROM kinds")

    kinds= cur.fetchall()
    kind=[]
    for k in kinds:
       kind.append([k[0],k[1].split(",")])
    kinds=kind

    cur.close()
    return render_template('layout - Copy.html', sections= ordered_sections_with_products, kinds=kinds)

@app.route('/home')
def home():
    cur = mysql.connection.cursor()

    cur.execute("SELECT * FROM sections")

    sections= cur.fetchall()
    ordered_sections= order_by_section(sections)
    ordered_sections_with_products=[]

    for section in ordered_sections:
       section_name= section[0]
       section_products=section[1]
       temp=[]
       for id in section_products:
         cur.execute("SELECT product_id, name, price, descreption, qte, pictures FROM products WHERE product_id = %s", (id,))

         products = cur.fetchall()
         #products[5]=products[5].split(',')
         product=[products[0][0],products[0][1],products[0][2],products[0][3],products[0][4],products[0][5].split(',')]
         temp.append(product)
         
         #print(products[0][5].split(','))
         #print(products[0])
      
       #print(temp)
       ordered_sections_with_products.append([section_name,temp])

    #print(pictures)


    cur.execute("SELECT * FROM kinds")

    kinds= cur.fetchall()
    kind=[]
    for k in kinds:
       kind.append([k[0],k[1].split(",")])
    kinds=kind

    cur.close()
    return render_template('layout - Copy.html', sections= ordered_sections_with_products,kinds = kinds)


@app.route('/run_my_code')
def run_my_code():
    # Create a cursor
    product_Id = request.args.get('product_id')
    cur = mysql.connection.cursor()

    # Execute a query to retrieve product information
    cur.execute("SELECT product_id, name, price, descreption, qte, pictures FROM products WHERE product_id = %s", (product_Id,))

    # Fetch all the product data
    products = cur.fetchall()
    pictures=[]
    for product in products:
        pictures= product[5].split(',')
    

    # Close the cursor
    cur.execute("SELECT * FROM kinds")

    kinds= cur.fetchall()
    kind=[]
    for k in kinds:
       kind.append([k[0],k[1].split(",")])
    kinds=kind

    #suggestions
    cur.execute("SELECT product_id, name, price, descreption, qte, pictures, kind FROM products WHERE product_id = %s", (product_Id,))
    suggested = cur.fetchall()
    cur.execute("SELECT product_id, name, price, descreption, qte, pictures, kind FROM products ")
    p=cur.fetchall()
    suggested_products=[]
    for prod in p:
       for kind in suggested[0][6].split(","):
         if kind in prod[6].split(","):
            suggestion=[prod[0],prod[1],prod[2],prod[3],prod[4],prod[5].split(',')]
            suggested_products.append(suggestion)
       


    cur.close()

    return render_template('landing.html', products=products, pictures=pictures, kinds=kinds,suggested_products = suggested_products)


@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        # Get customer information from the form
        name = request.form['name']
        address = request.form['address']
        phone_number = request.form['phone_number']

        # Create a cursor
        cur = mysql.connection.cursor()
        product_Id = request.form['product_id']
        print('product id :'+str(product_Id))

        # Insert customer information into the 'users' table
        cur.execute("INSERT INTO users (name, address, phone_number,product_id) VALUES (%s, %s, %s,%s)", (name, address, phone_number,product_Id))
        

        # Commit changes and close the cursor
        mysql.connection.commit()
        cur.close()

        return render_template("thank_you.html")


def common_letters(mot1,mot2):#search_suery, our words
   cpt=0
   for i in mot1:
      if i in(mot2):
         cpt+=1
   return cpt 
      

def poids(list,search_query):
   name=list[1]
   kinds=list[2].split(',')
   search_query_poids=0
   if name == search_query or list[0] == search_query:
      search_query_poids=100
   else:
      for kind in kinds:
         search_query_poids += common_letters(search_query,kind)
      search_query_poids += common_letters(search_query,name)
   return [list[0],search_query_poids]

def search_results(search_query, data):
   result=[]
   for product in data : 
      result.append(poids(product,search_query))
   for i in range(len(result)):
     product = result[i]
     max = product[1]
     print(max)
     for j in range(i,len(result)):
         if result[j][1] > max:
           max= result[j][1]
           x = product
           result[i] = result[j]
           result[j] = x
           product=result[i]
   return result

         
         

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        search_query = request.form.get('query')  # Get the search query from the form data

        cur = mysql.connection.cursor()

       # Execute a query to retrieve product information
        cur.execute("SELECT product_id, name,kind FROM products ")

        # Fetch all the product data
        products = cur.fetchall()

        searched_products_id=search_results(search_query,products)

        products_list=[]
        for product in searched_products_id:
           if product[1]>3 :
             cur.execute("SELECT product_id, name, price, descreption, qte, pictures FROM products WHERE product_id = %s", (product[0],))
             products = cur.fetchall()
             product_to_append=[products[0][0],products[0][1],products[0][2],products[0][3],products[0][4],products[0][5].split(',')]
             products_list.append(product_to_append)
      
        cur.execute("SELECT * FROM kinds")

        kinds= cur.fetchall()
        kind=[]
        for k in kinds:
          kind.append([k[0],k[1].split(",")])
        kinds=kind

        cur.close()

        return render_template('search.html', search_query=search_query,products_list= products_list, kinds = kinds)
    #return 'Search Page'

@app.route('/section_page')
def section_page():
    #section_value = request.args.get('section_value')
    section_value = request.args.get('section_value')
    cur = mysql.connection.cursor()

    cur.execute("SELECT product_id FROM sections WHERE section_name = %s ",(section_value,))
    products = cur.fetchall()
    print(products)
    sections_products=[]
    for id in products:
       cur.execute("SELECT product_id, name, price, descreption, qte, pictures FROM products WHERE product_id = %s", (id[0],))
       p = cur.fetchall()
       product_to_append=[p[0][0],p[0][1],p[0][2],p[0][3],p[0][4],p[0][5].split(',')]
       sections_products.append(product_to_append)
    #print(sections_products)
    


    cur.execute("SELECT * FROM kinds")

    kinds= cur.fetchall()
    kind=[]
    for k in kinds:
       kind.append([k[0],k[1].split(",")])
    kinds=kind
    
    cur.close()
    return render_template("section.html", section_value = section_value, sections_products = sections_products, kinds = kinds )

@app.route('/kind')
def kind():
    kind_value = request.args.get('kind_value')
    cur = mysql.connection.cursor()

    cur.execute("SELECT product_id, kind , sub_kind FROM products")
    products = cur.fetchall()
    print(products)
    kind_products=[]
    for product in products:
       if kind_value in product[1].split(",") or kind_value in product[2].split(","):
            cur.execute("SELECT product_id, name, price, descreption, qte, pictures FROM products WHERE product_id = %s", (product[0],))
            p = cur.fetchall()
            product_to_append=[p[0][0],p[0][1],p[0][2],p[0][3],p[0][4],p[0][5].split(',')]
            kind_products.append(product_to_append)
    
    cur.execute("SELECT * FROM kinds")

    kinds= cur.fetchall()
    kind=[]
    for k in kinds:
       kind.append([k[0],k[1].split(",")])
    kinds=kind

    cur.close()
    return render_template("kind.html", kind_value = kind_value, kind_products = kind_products, kinds = kinds)

if __name__ == '__main__':
    app.run()
