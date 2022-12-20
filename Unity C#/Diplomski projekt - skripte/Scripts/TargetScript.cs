using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Tobii.G2OM;

public class TargetScript : MonoBehaviour, IGazeFocusable
{    
    //private static readonly int _baseColor = Shader.PropertyToID("_BaseColor");
    //private Color _originalColor = Color.white;
    //private Color highlightColor = Color.green;
    //private Color _targetColor;
    //private Renderer _renderer;
    //public float animationTime = 0.1f;
    private float timer = 0f;
    private float timeToFocus = 0f;

    //skripta koja ocitava da li korisnik gleda u metu putem HTC vive eye-a. Koristi TobiiXR
    public void GazeFocusChanged(bool hasFocus)
        {
            if (timeToFocus == 0f) timeToFocus = timer; //zapisuje vrijeme do pogleda
            //Objekt je u fokusu - moze se unistiti s metkom
            /* if (hasFocus)
            {
                destroyable = true;
                //_targetColor = highlightColor;
            }
            //Nije u fokusu
            else
            {
                destroyable = false;
                //_targetColor = _originalColor;
            } */
        }


    // Start is called before the first frame update
    void Start()
    {

        /*
        _renderer = GetComponent<Renderer>();
        _renderer.material.color = _originalColor;
        _targetColor = _originalColor;
        */

    }

    // Update is called once per frame
    void Update()
    {
        timer += Time.deltaTime; //stoperica


        /*
        if (_renderer.material.HasProperty(_baseColor)) // new rendering pipeline (lightweight, hd, universal...)
        {
            _renderer.material.SetColor(_baseColor, Color.Lerp(_renderer.material.GetColor(_baseColor), _targetColor, Time.deltaTime * (1 / animationTime)));
        }
        else // old standard rendering pipline
        {
            _renderer.material.color = Color.Lerp(_renderer.material.color, _targetColor, Time.deltaTime * (1 / animationTime));
        }
        */

        /*if (destroyable) {
            timer += Time.deltaTime;
            if (timer >1f) Death();
        } else timer = 0f;*/
    }

    public void Death() {
        Instantiate(Resources.Load("Prefabs/Target explosion"), transform.position, transform.rotation);
        Instantiate(Resources.Load("Prefabs/Target smoke"), transform.position, transform.rotation);
        GameObject.FindGameObjectWithTag("EventHandler").GetComponent<EventsSystem>().TargetData(timeToFocus, timer, true); //javlja event systemu podatke
        Destroy(this.gameObject);
    }
    private void OnTriggerEnter(Collider other) {
        if (other.tag == "Player") {
            Death();
        }
    }
    
    public void EndOfGameDeath() {
        Destroy(this.gameObject);
    }
}
