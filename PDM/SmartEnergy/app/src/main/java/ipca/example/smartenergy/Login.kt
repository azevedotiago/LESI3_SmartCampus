package ipca.example.smartenergy

import android.content.Intent
import android.os.Bundle
import android.widget.Button
import android.widget.EditText
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.lifecycle.lifecycleScope
import okhttp3.OkHttpClient


class Login : AppCompatActivity() {

    var loginmethod = "login"
    var loginResponse: Boolean = false

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        try {
            this.supportActionBar!!.hide()
        } catch (e: NullPointerException) {
        }

        setContentView(R.layout.login)

        // atribuir referencias as Views
        var et_user_name = findViewById<EditText>(R.id.et_user_name)
        var et_password = findViewById<EditText>(R.id.et_password)
        var btn_reset = findViewById<Button>(R.id.btn_reset)
        var btn_submit = findViewById<Button>(R.id.btn_submit)

        btn_reset.setOnClickListener {
            // quando se clicar no botao Cancelar apaga os campos username e password
            et_user_name.setText("")
            et_password.setText("")
        }

        // set on-click listener
        btn_submit.setOnClickListener {
            val username = et_user_name.text;
            val password = et_password.text;

            //println("#### login  : Backend.login...")
            Backend.login(lifecycleScope, loginmethod, username, password){
                if (it) {       // login ok
                    Toast.makeText(this@Login, "Autenticando com o utilizador $username", Toast.LENGTH_LONG).show()
                    // ir para a MainActivity
                    val intent = Intent(this@Login, MainActivity::class.java)
                    startActivity(intent)
                } else {        // login sem sucesso
                    Toast.makeText(this@Login, "Erro na autenticação!", Toast.LENGTH_LONG).show()
                }
            }
        }
    }
}