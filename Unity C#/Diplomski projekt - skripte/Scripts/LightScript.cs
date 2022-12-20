using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Tobii.G2OM;

public class LightScript : MonoBehaviour, IGazeFocusable
{
    private static readonly int _baseColor = Shader.PropertyToID("_BaseColor");
    private Color _originalColor;
    private Color selectedColor = Color.yellow;
    private Color focusColor = Color.green;
    private Color _targetColor;
    private Renderer _renderer;
    public float animationTime = 0.1f;

    private bool target = false;
    private bool isFocused = false;
    private bool button = false;
    public bool CameraDetector = false;
    private GameObject EH;

    private float timerFocus = 0f;
    private float timer = 0f;

    public void GazeFocusChanged(bool hasFocus) {
        if (hasFocus)
        {
            isFocused = true;
            if (target) {
                if (timerFocus == 0f) timerFocus = timer;
                _targetColor = focusColor;
            }
        }
        //Nije u fokusu
        else
        {
            isFocused = false;
            if (target) 
                _targetColor = selectedColor;
            else
                _targetColor = _originalColor;
        }
    }

    // Start is called before the first frame update
    void Start()
    {
        _renderer = GetComponent<Renderer>();
        _originalColor = _renderer.material.color;
        _targetColor = _originalColor;
        EH = GameObject.FindWithTag("EventHandler");
    }

    // Update is called once per frame
    void Update()
    {
        if (target) {
            timer += Time.deltaTime;
        }
        if (_renderer.material.HasProperty(_baseColor)) // new rendering pipeline (lightweight, hd, universal...)
        {
            _renderer.material.SetColor(_baseColor, Color.Lerp(_renderer.material.GetColor(_baseColor), _targetColor, Time.deltaTime * (1 / animationTime)));
        }
        else // old standard rendering pipline
        {
            _renderer.material.color = Color.Lerp(_renderer.material.color, _targetColor, Time.deltaTime * (1 / animationTime));
        }
        if (button) {
            button = false;
            if (target && isFocused) {
                EH.GetComponent<EventsSystem>().AddButtonScore(timerFocus, timer);
            } else {
                EH.GetComponent<EventsSystem>().AddButtonWrongScore(timer);
            }
        }
    }


    public void SetLight(bool b) {
        timer = 0f;
        timerFocus = 0f;
        target = b;
        if (target) {
            _targetColor = Color.yellow; //zbog nekog razloga ne radi dobro sa selectedColor 
        } else {
            _targetColor = _originalColor;
        }
    }

    public void Button() {
        button = true;
    }
}
