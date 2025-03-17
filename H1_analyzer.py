class H1Analyzer:
    def identify_key_levels(self, data):
        """Identifica niveles clave de soporte y resistencia en 1H"""
        levels = []
        
        highs = data['High'].rolling(window=3, center=True).max()
        lows = data['Low'].rolling(window=3, center=True).min()
        
        for i in range(1, len(data) - 1):
            if data['High'][i] == highs[i]:  # Resistencia
                levels.append({'Date': data['Date'][i], 'Level': highs[i], 'Type': 'Resistance'})
            elif data['Low'][i] == lows[i]:  # Soporte
                levels.append({'Date': data['Date'][i], 'Level': lows[i], 'Type': 'Support'})
        
        return levels
    
    def analyze_polarity(self, data, levels):
        """Analiza cambios de polaridad en los niveles clave"""
        polarities = []
        
        for level in levels:
            # Buscar rupturas y cambios de polaridad
            breakouts = self._find_breakouts(data, level)
            
            for breakout in breakouts:
                # Identificar si hubo cambio de polaridad después del breakout
                polarity_change = self._check_polarity_change(data, level, breakout)
                
                if polarity_change:
                    # Identificar qué esquema aplica (Doble, Trampa, Falla, Continuación)
                    scheme = self._identify_scheme(data, level, breakout, polarity_change)
                    
                    polarities.append({
                        'level': level['Level'],
                        'original_type': level['Type'],
                        'new_type': 'Resistance' if level['Type'] == 'Support' else 'Support',
                        'breakout_index': breakout['index'],
                        'direction': 'Sell' if level['Type'] == 'Support' else 'Buy',
                        'scheme': scheme
                    })
        
        return polarities
    
    def analyze_breakout_support(self, data, levels):
        """Analiza apoyo en nivel de rompimiento"""
        breakout_supports = []
        
        for level in levels:
            # Buscar rupturas claras
            breakouts = self._find_strong_breakouts(data, level)
            
            for breakout in breakouts:
                # Buscar retests después del breakout
                retests = self._find_retests(data, level, breakout)
                
                for retest in retests:
                    # Comprobar si el nivel actúa como apoyo para la continuación
                    if self._check_continuation(data, level, breakout, retest):
                        # Identificar esquema (Doble, Trampa, Falla, Continuación)
                        scheme = self._identify_scheme(data, level, breakout, retest)
                        
                        breakout_supports.append({
                            'level': level['Level'],
                            'original_type': level['Type'],
                            'breakout_index': breakout['index'],
                            'retest_index': retest['index'],
                            'direction': 'Buy' if level['Type'] == 'Resistance' else 'Sell',
                            'scheme': scheme
                        })
        
        return breakout_supports
    
    # Métodos auxiliares (implementación necesaria)
    def _find_breakouts(self, data, level):
        """Busca rupturas de un nivel"""
        breakouts = []
        for i in range(1, len(data) - 1):
            if level['Type'] == 'Resistance' and data['High'][i] > level['Level']:
                breakouts.append({'index': i, 'price': data['High'][i]})
            elif level['Type'] == 'Support' and data['Low'][i] < level['Level']:
                breakouts.append({'index': i, 'price': data['Low'][i]})
        return breakouts
    
    def _check_polarity_change(self, data, level, breakout):
        """Verifica si hubo cambio de polaridad después de una ruptura"""
        if level['Type'] == 'Resistance' and data['Close'][breakout['index']] > level['Level']:
            return True
        elif level['Type'] == 'Support' and data['Close'][breakout['index']] < level['Level']:
            return True
        return False
    
    def _identify_scheme(self, data, level, breakout, event):
        """Identifica qué esquema aplica (Doble, Trampa, Falla, Continuación)"""
        if event:
            if level['Type'] == 'Resistance':
                if data['High'][breakout['index']] == data['High'][breakout['index'] - 2]:
                    return 'Doble'
                elif data['High'][breakout['index']] > data['High'][breakout['index'] - 1]:
                    return 'Trampa'
                elif data['High'][breakout['index']] < data['High'][breakout['index'] - 1]:
                    return 'Falla'
                else:
                    return 'Continuación'
            elif level['Type'] == 'Support':
                if data['Low'][breakout['index']] == data['Low'][breakout['index'] - 2]:
                    return 'Doble'
                elif data['Low'][breakout['index']] < data['Low'][breakout['index'] - 1]:
                    return 'Trampa'
                elif data['Low'][breakout['index']] > data['Low'][breakout['index'] - 1]:
                    return 'Falla'
                else:
                    return 'Continuación'
        return 'Desconocido'
    
    def _find_strong_breakouts(self, data, level):
        """Busca rupturas fuertes y claras de un nivel"""
        breakouts = []
        for i in range(1, len(data) - 1):
            if level['Type'] == 'Resistance' and data['High'][i] > level['Level'] and data['Close'][i] > level['Level']:
                breakouts.append({'index': i, 'price': data['High'][i]})
            elif level['Type'] == 'Support' and data['Low'][i] < level['Level'] and data['Close'][i] < level['Level']:
                breakouts.append({'index': i, 'price': data['Low'][i]})
        return breakouts
    
    def _find_retests(self, data, level, breakout):
        """Busca retests después de una ruptura"""
        retests = []
        for i in range(breakout['index'] + 1, len(data) - 1):
            if level['Type'] == 'Resistance' and data['Low'][i] <= level['Level']:
                retests.append({'index': i, 'price': data['Low'][i]})
            elif level['Type'] == 'Support' and data['High'][i] >= level['Level']:
                retests.append({'index': i, 'price': data['High'][i]})
        return retests
    
    def _check_continuation(self, data, level, breakout, retest):
        """Verifica si hay continuación después del retest"""
        if level['Type'] == 'Resistance' and data['Close'][retest['index']] > level['Level']:
            return True
        elif level['Type'] == 'Support' and data['Close'][retest['index']] < level['Level']:
            return True
        return False