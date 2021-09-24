if __name__ == '__main__':
    import uvicorn
    uvicorn.run('demo.app:app', port=5000, debug=True)
