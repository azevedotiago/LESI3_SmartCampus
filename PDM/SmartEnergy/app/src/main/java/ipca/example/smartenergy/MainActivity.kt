package ipca.example.smartenergy

import android.annotation.SuppressLint
import android.content.Intent
import android.graphics.Color
import android.os.Bundle
import android.os.Handler
import android.util.Log
import android.view.Menu
import android.view.MenuItem
import android.view.View
import android.view.ViewGroup
import android.widget.*
import androidx.appcompat.app.AppCompatActivity
import androidx.lifecycle.lifecycleScope
import java.time.LocalDateTime
import java.time.format.DateTimeFormatter


class MainActivity : AppCompatActivity() {
    // model
    var devices     = arrayListOf<Device>()
    val adapter     = DevicesAdapter()
    var delay       = 20000                             // numero de segundos * 1000 para fazer o refresh
    var current     = LocalDateTime.now()               // data hora atual
    val formatter   = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss")

    private var handler: Handler = Handler()
    private var runnable: Runnable? = null

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        // remover a barra de título da aplicação
        // try { this.supportActionBar!!.hide() } catch (e: NullPointerException) { }

        title = "Lista de dispositivos | atualizado em " + current.format(formatter)
        setContentView(R.layout.activity_main)

        Backend.fetchDevices(lifecycleScope, "select","devicesstatus"){
            devices = it
            adapter.notifyDataSetChanged()
        }
        val listViewDevice = findViewById<ListView>(R.id.listViewDevices)
        listViewDevice.adapter = adapter
    }

    override fun onResume() {       // de 15 em 15 segundos faz um refresh da view atual, atualiza os dados dos DEVICES
        handler.postDelayed(Runnable {
            runnable?.let {
                handler.postDelayed(it, delay.toLong())
                Backend.fetchDevices(lifecycleScope, "select","devicesstatus"){
                    devices = it
                    adapter.notifyDataSetChanged()
                    this.current = LocalDateTime.now()
                    title = "Lista de dispositivos | atualizado em "+ current.format(formatter)
                }
            }
            Toast.makeText(
                this@MainActivity, "Atualizando dispositivos a cada " + delay / 1000 +" segundos",
                Toast.LENGTH_SHORT
            ).show()
        }.also { runnable = it }, delay.toLong())
        super.onResume()
    }

    override fun onPause() {
        super.onPause()
        runnable?.let { handler.removeCallbacks(it) } //stop handler when activity not visible super.onPause();
    }

    inner class DevicesAdapter : BaseAdapter() {
        override fun getCount(): Int {
           return devices.size
        }

        override fun getItem(positon: Int): Any {
            return devices[positon]
        }

        override fun getItemId(positon: Int): Long {
            return 0L
        }

        @SuppressLint("SetTextI18n")
        override fun getView(position: Int, view: View?, parent: ViewGroup?): View {
            val rowView = layoutInflater.inflate(R.layout.row_device,parent, false)
            val textViewDeviceID = rowView.findViewById<TextView>(R.id.textViewDeviceID)
            val textViewDeviceMacAddress = rowView.findViewById<TextView>(R.id.textViewDeviceMacAddress)
            val textViewDeviceDetail = rowView.findViewById<TextView>(R.id.textViewDeviceDetail)
            val textViewDeviceCoord = rowView.findViewById<TextView>(R.id.textViewDeviceCoord)
            val textViewDeviceStatus = rowView.findViewById<TextView>(R.id.textViewDeviceStatus)

            val device = devices[position]
            //println("#### MainActivity | devices[position]: "+position%2)
            if (position % 2 == 0 ) {
                // nas ROWS pares coloca o fundo (background) a cinza claro
                rowView.setBackgroundColor(Color.parseColor("#f6f6f6"))
            }
            textViewDeviceID.text = device.iddevices
            textViewDeviceMacAddress.text = device.macaddress
            textViewDeviceDetail.text = device.detail
            textViewDeviceCoord.text = device.coordinatex+", "+ device.coordinatey
            textViewDeviceStatus.text = device.status
            if (device.status=="offline") {
                // cor do texto vermelho para o estado offline
                textViewDeviceStatus.setTextColor(Color.parseColor("#E91E63"));
            } else {
                // cor do texto verde para o estado online
                textViewDeviceStatus.setTextColor(Color.parseColor("#228B22"));
            }

            rowView.setOnClickListener {
                Log.d(TAG, "device:${device.iddevices}")
                //println("#### rowView.setOnClickListner | iddevices: " +device.iddevices )
                val intent = Intent(this@MainActivity, DeviceWebDetailActivity::class.java)
                intent.putExtra(EXTRA_ARTICLE, device.toJSON().toString())
                //println("#### rowView.setOnClickListner | intent: "+device.toJSON().toString())
                startActivity(intent)
            }
            return rowView
        }
    }

    override fun onCreateOptionsMenu(menu: Menu?): Boolean {
        menuInflater.inflate(R.menu.menu_device,menu)
        return true
    }

    override fun onOptionsItemSelected(item: MenuItem): Boolean {
        return when(item.itemId){
            R.id.action_share -> {
                Toast.makeText(this, "SmartEnergy", Toast.LENGTH_LONG).show()
                return true
            }
            else -> super.onOptionsItemSelected(item)
        }
    }

    companion object {
        const val TAG = "MainActivity"
        const val EXTRA_ARTICLE = "extra_article"
    }
}