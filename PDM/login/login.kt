package ipca.budget.smartenergy
// https://github.com/jayfirke/Login-With-Kotlin-and-Php-MySQL
// https://androidjson.com/android-server-login-registration-php-mysql/

// https://www.tutorialkart.com/kotlin-android/login-form-example-in-kotlin-android/

// remover o titulo da app na janela de login
// https://stackoverflow.com/questions/36236181/how-to-remove-title-bar-from-the-android-activity

import android.os.Bundle
import android.support.v7.app.AppCompatActivity
import android.view.textclassifier.TextLinks
import android.widget.Button
import android.widget.EditText
import android.widget.Toast
import okhttp3.OkHttpClient
import okhttp3.Request
import org.json.JSONObject
import java.io.IOException




@Suppress("DEPRECATION")
class MainActivity : AppCompatActivity() {

    var loginmethod = "login"
    var server = "10.10.10.2"
    private val client = OkHttpClient()

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
            Toast.makeText(this@MainActivity, username, Toast.LENGTH_LONG).show()

            // codigo para verificar a combinacao username e password
            var url =
                "http://" + server + ":80/login.php?method=" + loginmethod + "&username=" + username + "&password=" + password
            println("username: " + username)
            println("password: " + password)
            println("url     : " + url)

            //creating a string request
            println("result  : fetching...")
            val request = Request.Builder().url(url).build()
            client.newCall(request).execute().use { response ->
                if (!response.isSuccessful) throw IOException("Unexpected code $response")

                val result =  response.body!!.string()
                //Log.d(MainActivity.TAG, result)

                val jsonObject = JSONObject(result)
                if (jsonObject.getString("response") == "true"){
                    println("### login: ok")
                }
            }

        }
    }
}