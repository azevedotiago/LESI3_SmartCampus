package ipca.budget.smartenergy
// https://github.com/jayfirke/Login-With-Kotlin-and-Php-MySQL
// https://androidjson.com/android-server-login-registration-php-mysql/

// https://www.tutorialkart.com/kotlin-android/login-form-example-in-kotlin-android/

// remover o titulo da app na janela de login
// https://stackoverflow.com/questions/36236181/how-to-remove-title-bar-from-the-android-activity


import android.os.Bundle
import android.support.v7.app.AppCompatActivity
import android.widget.Button
import android.widget.EditText
import android.widget.Toast

class MainActivity : AppCompatActivity() {

    var loginmethod = "login"
    var server = "10.10.10.2"

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        try {
            this.supportActionBar!!.hide()
        } catch (e: NullPointerException) {
        }

        setContentView(R.layout.activity_main)

        // atribuir referencias as Views
        var et_user_name = findViewById(R.id.et_user_name) as EditText
        var et_password = findViewById(R.id.et_password) as EditText
        var btn_reset = findViewById(R.id.btn_reset) as Button
        var btn_submit = findViewById(R.id.btn_submit) as Button

        btn_reset.setOnClickListener {
            // quando se clicar no botao Cancelar apaga os campos username e password
            et_user_name.setText("")
            et_password.setText("")
        }

        // set on-click listener
        btn_submit.setOnClickListener {
            val username = et_user_name.text;
            val password = et_password.text;
            Toast.makeText(this@MainActivity, user_name, Toast.LENGTH_LONG).show()

            // codigo para verificar a combinacao username e password
            var username = username_Et.text.toString()
            var password = password_Et.text.toString()
            var URL_ROOT = "http://"+server+":80/login.php?method=" + loginmethod + "&username=" + username + "&password=" + password
            println("username: " + username)
            println("password: " + password)
            println("url     : " + URL_ROOT)


        }
    }
}