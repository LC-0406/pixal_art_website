class PixelCanvas {
    constructor(canvasId, options = {}) {
        this.canvas = document.getElementById(canvasId);
        this.ctx = this.canvas.getContext('2d');
        this.gridSize = options.gridSize || 32;
        this.pixelSize = options.pixelSize || 20;
        this.gridData = options.gridData || this.createEmptyGrid();
        this.currentColor = options.defaultColor || '#000000';
        this.isDrawing = false;
        this.editable = options.editable || false;
        this.canvasId = options.canvasId;
        
        this.init();
    }
    
    createEmptyGrid() {
        return Array(this.gridSize).fill().map(() => 
            Array(this.gridSize).fill(null)
        );
    }
    
    init() {
        this.updateCanvasSize();
        this.renderGrid();
        
        if (this.editable) {
            this.setupEventListeners();
            this.setupColorPicker();
        }
    }
    
    updateCanvasSize() {
        this.canvas.width = this.gridSize * this.pixelSize;
        this.canvas.height = this.gridSize * this.pixelSize;
    }
    
    renderGrid() {
        // 清空画布
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        
        // 绘制网格线
        this.ctx.strokeStyle = '#ddd';
        this.ctx.lineWidth = 1;
        
        for (let x = 0; x <= this.gridSize; x++) {
            this.ctx.beginPath();
            this.ctx.moveTo(x * this.pixelSize, 0);
            this.ctx.lineTo(x * this.pixelSize, this.canvas.height);
            this.ctx.stroke();
        }
        
        for (let y = 0; y <= this.gridSize; y++) {
            this.ctx.beginPath();
            this.ctx.moveTo(0, y * this.pixelSize);
            this.ctx.lineTo(this.canvas.width, y * this.pixelSize);
            this.ctx.stroke();
        }
        
        // 绘制像素
        for (let y = 0; y < this.gridSize; y++) {
            for (let x = 0; x < this.gridSize; x++) {
                if (this.gridData[y][x]) {
                    this.ctx.fillStyle = this.gridData[y][x];
                    this.ctx.fillRect(
                        x * this.pixelSize,
                        y * this.pixelSize,
                        this.pixelSize,
                        this.pixelSize
                    );
                }
            }
        }
    }
    
    setupEventListeners() {
        this.canvas.addEventListener('mousedown', (e) => {
            if (!this.editable) return;
            this.isDrawing = true;
            this.drawAtPosition(e);
        });
        
        this.canvas.addEventListener('mousemove', (e) => {
            if (!this.editable || !this.isDrawing) return;
            this.drawAtPosition(e);
        });
        
        this.canvas.addEventListener('mouseup', () => {
            this.isDrawing = false;
            this.saveToServer();
        });
        
        this.canvas.addEventListener('mouseleave', () => {
            this.isDrawing = false;
        });
    }
    
    setupColorPicker() {
        const colorPicker = document.getElementById('colorPicker');
        if (colorPicker) {
            colorPicker.addEventListener('input', (e) => {
                this.currentColor = e.target.value;
            });
            
            const colorButtons = document.querySelectorAll('.color-btn');
            colorButtons.forEach(btn => {
                btn.addEventListener('click', (e) => {
                    this.currentColor = e.target.dataset.color;
                    colorPicker.value = this.currentColor;
                });
            });
        }
    }
    
    drawAtPosition(event) {
        const rect = this.canvas.getBoundingClientRect();
        const x = Math.floor((event.clientX - rect.left) / this.pixelSize);
        const y = Math.floor((event.clientY - rect.top) / this.pixelSize);
        
        if (x >= 0 && x < this.gridSize && y >= 0 && y < this.gridSize) {
            this.gridData[y][x] = this.currentColor;
            this.renderGrid();
        }
    }
    
    async saveToServer() {
        if (!this.canvasId) return;
        
        try {
            const response = await fetch(`/api/canvas/${this.canvasId}/update`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    gridData: this.gridData
                })
            });
            
            if (!response.ok) {
                throw new Error('保存失败');
            }
            
            const data = await response.json();
            if (data.success) {
                this.showMessage('保存成功', 'success');
            }
        } catch (error) {
            this.showMessage('保存失败: ' + error.message, 'error');
        }
    }
    
    showMessage(message, type) {
        // 实现消息提示
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type}`;
        alertDiv.textContent = message;
        
        document.querySelector('main').prepend(alertDiv);
        
        setTimeout(() => {
            alertDiv.remove();
        }, 3000);
    }
}

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', function() {
    const canvasElement = document.getElementById('pixelCanvas');
    if (canvasElement) {
        const gridData = JSON.parse(canvasElement.dataset.gridData || '[]');
        const canvasId = canvasElement.dataset.canvasId;
        const editable = canvasElement.dataset.editable === 'true';
        
        new PixelCanvas('pixelCanvas', {
            gridSize: parseInt(canvasElement.dataset.gridSize) || 32,
            pixelSize: parseInt(canvasElement.dataset.pixelSize) || 20,
            gridData: gridData,
            editable: editable,
            canvasId: canvasId
        });
    }
});